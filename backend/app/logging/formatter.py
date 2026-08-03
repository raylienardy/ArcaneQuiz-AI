import json
import logging
from datetime import datetime, timezone

class JsonFormatter(logging.Formatter):
    """Formatter yang menghasilkan JSON string dari log record (jika log data adalah dict)."""
    def format(self, record: logging.LogRecord) -> str:
        if isinstance(record.msg, dict):
            base = record.msg.copy()
            base["timestamp"] = datetime.now(timezone.utc).isoformat()
            base["level"] = record.levelname
            return json.dumps(base)
        return super().format(record)