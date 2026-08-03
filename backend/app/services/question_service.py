import time
import logging
import asyncio
from datetime import datetime, timezone
from .ai_service import AIService
from ..question_generator.prompt_builder import PromptBuilder
from ..question_generator.models import QuestionRequest, QuestionResponse
from ..question_generator.json_parser import JSONResponseParser
from ..question_generator.validators import QuestionValidator
from ..question_generator.token_utils import truncate_text, estimate_tokens
from ..ai.models import AIRequest
from ..logging import GenerationContext
from ..logging.logger import (
    log_generation_started,
    log_prompt_built,
    log_provider_selected,
    log_request_sent,
    log_response_received,
    log_json_parsed,
    log_validation_started,
    log_validation_completed,
    log_generation_completed,
    log_generation_failed,
)

logger = logging.getLogger(__name__)

PROMPT_VERSION = "v1"
SCHEMA_VERSION = "1.0"
AI_TIMEOUT = 60  # detik

class QuestionService:
    def __init__(self):
        self.ai_service = AIService()
        self.prompt_builder = PromptBuilder()
        self.parser = JSONResponseParser()
        self.validator = QuestionValidator()
        self._last_prompt = None
        self.debug_info = {}

    async def generate_questions(self, request: QuestionRequest, debug: bool = False) -> QuestionResponse:
        # Buat konteks baru untuk request ini
        ctx = GenerationContext(
            session_id=str(id(request)),
            prompt_version=PROMPT_VERSION,
            schema_version=SCHEMA_VERSION,
        )
        log_generation_started(ctx)
        total_start = time.time()
        self.debug_info = {}  # reset

        # Potong teks jika terlalu besar
        original_text = request.text
        truncated_text, was_truncated = truncate_text(original_text, max_tokens=5000)
        if was_truncated:
            logger.warning("Document truncated to 5000 tokens to avoid rate limit.")
            # Buat ulang request dengan teks yang sudah dipotong (aman untuk Pydantic v1 dan v2)
            request = QuestionRequest(
                text=truncated_text,
                question_type=request.question_type,
                number_of_questions=request.number_of_questions,
                difficulty=request.difficulty,
                language=request.language,
                additional_instruction=request.additional_instruction,
                metadata=request.metadata,
            )

        try:
            # 1. Prompt
            prompt = self.prompt_builder.build(request)
            self._last_prompt = prompt
            log_prompt_built(ctx)
            if debug:
                self.debug_info["prompt"] = {
                    "text": prompt,
                    "prompt_version": PROMPT_VERSION,
                    "language": request.language,
                    "question_type": request.question_type.value,
                    "difficulty": request.difficulty.value if request.difficulty else None,
                    "question_count": request.number_of_questions,
                }

            # 2. Provider info
            await self.ai_service.initialize()
            ctx.provider = self.ai_service.provider_name
            log_provider_selected(ctx)

            # 3. Kirim request
            ai_request = AIRequest(
                prompt=prompt,
                temperature=0.7,
                max_tokens=2048,
                metadata={"number_of_questions": request.number_of_questions},  # ← tambahkan
            )
            start_time = log_request_sent(ctx)

            try:
                ai_response = await asyncio.wait_for(
                    self.ai_service.generate(ai_request),
                    timeout=AI_TIMEOUT
                )
            except asyncio.TimeoutError:
                log_generation_failed(ctx, "AI request timed out", "TimeoutError")
                raise
            except Exception as e:
                log_generation_failed(ctx, str(e), type(e).__name__)
                raise

            elapsed_request = log_response_received(ctx, start_time)
            ctx.model = ai_response.metadata.get("model", "unknown")
            if debug:
                self.debug_info["provider"] = {
                    "provider": ai_response.provider,
                    "model": ctx.model,
                    "temperature": 0.7,
                    "max_tokens": 2048,
                    "latency_seconds": elapsed_request,
                }
                self.debug_info["raw_response"] = ai_response.response_text

            # 4. Parsing
            try:
                question_response = self.parser.parse(ai_response.response_text)
                log_json_parsed(ctx)
                if debug:
                    self.debug_info["parsed_json"] = question_response.model_dump()
            except Exception as e:
                if debug:
                    self.debug_info["parser"] = {"status": "failed", "error": str(e)}
                log_generation_failed(ctx, str(e), "ParserError")
                raise

            # 5. Validasi
            log_validation_started(ctx)
            try:
                self.validator.validate(question_response)
                log_validation_completed(ctx, True)
                if debug:
                    self.debug_info["validation"] = {"status": "passed", "errors": []}
            except Exception as e:
                log_validation_completed(ctx, False, [str(e)])
                if debug:
                    self.debug_info["validation"] = {"status": "failed", "errors": [str(e)]}
                raise

            # Isi metadata dan selesaikan
            question_response.provider = ai_response.provider
            question_response.model = ctx.model
            question_response.generation_time = elapsed_request
            question_response.metadata.update({
                "prompt_version": PROMPT_VERSION,
                "schema_version": SCHEMA_VERSION,
                "generation_timestamp": datetime.now(timezone.utc).isoformat(),
            })
            if "usage" in ai_response.metadata:
                question_response.metadata["token_usage"] = ai_response.metadata["usage"]
            if "finish_reason" in ai_response.metadata:
                question_response.metadata["finish_reason"] = ai_response.metadata["finish_reason"]

            total_elapsed = time.time() - total_start
            log_generation_completed(ctx, len(question_response.questions), total_elapsed)
            if debug:
                self.debug_info["final_response"] = question_response.model_dump()

            return question_response

        except Exception as e:
            # Jika error tidak tertangani di atas, log di sini
            log_generation_failed(ctx, str(e), type(e).__name__)
            raise