import { useState, useEffect, useMemo } from "react";
import UploadCard from "../components/UploadCard";
import QuestionReviewWorkspace from "../components/questions/QuestionReviewWorkspace";
import QuestionAnalyticsPanel from "../components/questions/QuestionAnalyticsPanel";
import AIMetadataPanel from "../components/questions/AIMetadataPanel";
import AIPipelineInspector from "../components/debug/AIPipelineInspector";
import DeveloperToolbar from "../components/debug/DeveloperToolbar";
import LoadingMessage from "../components/feedback/LoadingMessage";
import RetryCard from "../components/feedback/RetryCard";
import EmptyState from "../components/feedback/EmptyState";
import SuccessState from "../components/feedback/SuccessState";
import GenerationSessionPanel from "../components/session/GenerationSessionPanel";
import ExportPreview from "../components/export/ExportPreview";
import { createSession } from "../session/generationSession";
import { uploadFile } from "../services/uploadService";
import { generateQuestions } from "../services/questionService";
import { validateFile } from "../utils/validateFile";
import "./UploadPage.css";

export default function UploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadState, setUploadState] = useState("idle");
  const [uploadResult, setUploadResult] = useState(null);
  const [uploadError, setUploadError] = useState(null);
  const [validationError, setValidationError] = useState(null);
  const [generationState, setGenerationState] = useState("idle");
  const [generatedQuestions, setGeneratedQuestions] = useState(null);
  const [generationMeta, setGenerationMeta] = useState(null);
  const [debugData, setDebugData] = useState(null);
  const [devMode, setDevMode] = useState(
    () => localStorage.getItem("devMode") === "true",
  );
  // state tambahan
  const [showExportPreview, setShowExportPreview] = useState(false);
  const [exportPreviewData, setExportPreviewData] = useState(null);
  // Tambahkan state di dalam komponen UploadPage
  const [showCountModal, setShowCountModal] = useState(false);
  const [questionCount, setQuestionCount] = useState(5); // default
  const [tempCount, setTempCount] = useState("5");
  const [countError, setCountError] = useState("");
  const API_BASE =
    import.meta.env.VITE_API_URL || "https://arcane-quiz-ai.vercel.app";

  // Fungsi untuk membuka modal
  const handleOpenCountModal = () => {
    setTempCount(String(questionCount));
    setCountError("");
    setShowCountModal(true);
  };

  const handleCountSubmit = () => {
    const trimmed = tempCount.trim();
    if (trimmed === "") {
      setCountError("Please enter a number.");
      return;
    }
    const num = Number(trimmed);
    if (isNaN(num) || !Number.isInteger(num)) {
      setCountError("Must be a whole number.");
      return;
    }
    if (num < 1) {
      setCountError("Minimum is 1 question.");
      return;
    }
    if (num > 20) {
      setCountError("Maximum is 20 questions (to avoid rate limits).");
      return;
    }
    setQuestionCount(num);
    setShowCountModal(false);
    // Otomatis panggil generate setelah validasi berhasil
    handleGenerate(num);
  };

  // fungsi untuk mengambil preview
  const handlePreviewExport = async (format = "pdf") => {
    if (!generatedQuestions) return;
    try {
      const response = await fetch(`${API_BASE}/export/preview`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          questions: generatedQuestions,
          format: format,
          metadata: generationMeta,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Export preview failed:", errorText);
        return;
      }

      const preview = await response.json();
      setExportPreviewData(preview);
      setShowExportPreview(true);
    } catch (error) {
      console.error("Failed to load preview:", error);
    }
  };

  const handleDownload = async () => {
    if (!generatedQuestions) return;
    try {
      const response = await fetch(`${API_BASE}/export/download`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          questions: generatedQuestions,
          format: "pdf",
          metadata: generationMeta || {},
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Download failed:", errorText);
        return;
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = exportPreviewData?.filename || "questions.pdf";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Download error:", error);
    }
  };

  // Bentuk session object secara memoized dari metadata dan questions
  const generationSession = useMemo(() => {
    if (generationState !== "success" || !generationMeta || !generatedQuestions)
      return null;
    return createSession({
      provider: generationMeta.provider,
      model: generationMeta.model,
      generationTime: generationMeta.latency_seconds,
      questionCount: generatedQuestions.length,
      language: "id", // bisa dari state, untuk sementara hardcode
      difficulty: "medium",
      questionType: "multiple_choice",
      promptVersion: generationMeta.prompt_version,
      schemaVersion: generationMeta.schema_version,
      status: "completed",
    });
  }, [generationState, generationMeta, generatedQuestions]);

  useEffect(() => {
    localStorage.setItem("devMode", devMode);
  }, [devMode]);

  const handleFileSelect = (file) => {
    const error = validateFile(file);
    setSelectedFile(file);
    setValidationError(error);
    setUploadState("idle");
    setUploadResult(null);
    setUploadError(null);
    resetGeneration();
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setValidationError(null);
    setUploadState("idle");
    setUploadResult(null);
    setUploadError(null);
    resetGeneration();
  };

  const resetGeneration = () => {
    setGenerationState("idle");
    setGeneratedQuestions(null);
    setGenerationMeta(null);
    setDebugData(null);
  };

  const handleUpload = async () => {
    if (!selectedFile || validationError) return;
    setUploadState("uploading");
    setUploadError(null);
    setUploadResult(null);
    resetGeneration();

    try {
      const data = await uploadFile(selectedFile);
      setUploadState("success");
      setUploadResult(data.data);
    } catch (error) {
      setUploadState("error");
      setUploadError(
        error?.response?.data?.detail ||
          error?.message ||
          "Upload failed. Please try again.",
      );
    }
  };

  const handleGenerate = async (customCount) => {
    const countToUse = customCount || questionCount;
    if (!uploadResult || !uploadResult.text) return;
    setGenerationState("generating");
    setUploadError(null);
    try {
      const payload = {
        text: uploadResult.text,
        question_type: "multiple_choice",
        number_of_questions: countToUse,
        difficulty: "medium",
        language: "id",
      };
      const response = await generateQuestions(payload, devMode);
      setGenerationState("success");
      setGeneratedQuestions(response.data.questions);
      setGenerationMeta(response.metadata);
      setDebugData(response.debug || null);
    } catch (error) {
      setGenerationState("error");
      setUploadError(error);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setValidationError(null);
    setUploadState("idle");
    setUploadResult(null);
    setUploadError(null);
    resetGeneration();
  };

  return (
    <div className="upload-page-container magical-bg">
      <div className="upload-header">
        <h1 className="arcane-title">📜 Arcane Forge</h1>
        <p className="arcane-subtitle">
          Transmute your documents into questions of power
        </p>
        <DeveloperToolbar devMode={devMode} onToggle={setDevMode} />
      </div>

      <div className="upload-section">
        <UploadCard
          file={selectedFile}
          onFileSelect={handleFileSelect}
          onRemove={handleRemoveFile}
          onUpload={handleUpload}
          uploadState={uploadState}
          uploadResult={uploadResult}
          uploadError={uploadError}
          validationError={validationError}
          onReset={handleReset}
        />
      </div>

      {uploadState === "uploading" && <LoadingMessage stage="upload" />}
      {uploadState === "error" && (
        <RetryCard error={uploadError} onRetry={handleUpload} />
      )}

      {uploadState === "success" && uploadResult && uploadResult.text && (
        <div className="generation-section">
          <button
            className="arcane-btn generate-btn"
            onClick={handleOpenCountModal}
            disabled={generationState === "generating"}
          >
            {generationState === "generating"
              ? "🔮 Generating..."
              : "✨ Generate Questions"}
          </button>

          {/* Modal input jumlah pertanyaan */}
          {showCountModal && (
            <div
              className="modal-overlay"
              onClick={() => setShowCountModal(false)}
            >
              <div
                className="modal-content count-modal"
                onClick={(e) => e.stopPropagation()}
              >
                <h3>📜 How many questions shall we conjure?</h3>
                <p className="modal-hint">Enter a number between 1 and 20.</p>
                <input
                  type="number"
                  className="arcane-input"
                  value={tempCount}
                  onChange={(e) => {
                    setTempCount(e.target.value);
                    setCountError("");
                  }}
                  onKeyDown={(e) => e.key === "Enter" && handleCountSubmit()}
                  min="1"
                  max="20"
                  autoFocus
                />
                {countError && <p className="count-error">{countError}</p>}
                <div className="modal-actions">
                  <button className="arcane-btn" onClick={handleCountSubmit}>
                    🔮 Conjure
                  </button>
                  <button
                    className="arcane-btn cancel-btn"
                    onClick={() => setShowCountModal(false)}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          )}

          {generationState === "generating" && (
            <LoadingMessage stage="generating" />
          )}
          {generationState === "error" && (
            <RetryCard error={uploadError} onRetry={handleGenerate} />
          )}

          {generationState === "success" && generatedQuestions && (
            <>
              <SuccessState message="Questions successfully conjured!" />
              <GenerationSessionPanel session={generationSession} />
              {devMode && (
                <AIPipelineInspector debugData={debugData} isOpen={devMode} />
              )}
              <QuestionAnalyticsPanel
                questions={generatedQuestions}
                provider={generationMeta?.provider}
                model={generationMeta?.model}
              />
              <AIMetadataPanel metadata={generationMeta} />
              <QuestionReviewWorkspace
                questions={generatedQuestions}
                onRegenerate={handleGenerate}
              />

              <div className="export-area">
                <button
                  className="arcane-btn"
                  onClick={() => handlePreviewExport("pdf")}
                >
                  📄 Export PDF
                </button>
              </div>

              {showExportPreview && exportPreviewData && (
                <div
                  className="modal-overlay"
                  onClick={() => setShowExportPreview(false)}
                >
                  <div
                    className="modal-content"
                    onClick={(e) => e.stopPropagation()}
                  >
                    <ExportPreview
                      previewData={exportPreviewData}
                      onDownload={handleDownload}
                    />
                    <button
                      className="arcane-btn close-btn"
                      onClick={() => setShowExportPreview(false)}
                    >
                      Close
                    </button>
                  </div>
                </div>
              )}
            </>
          )}

          {generationState === "idle" && !generatedQuestions && (
            <EmptyState
              title="Ready to conjure"
              description="Upload a document and cast the generation spell."
            />
          )}
        </div>
      )}

      <div className="supported-info">
        <p>
          Supported scrolls: <strong>PDF</strong>, <strong>DOCX</strong>,{" "}
          <strong>TXT</strong>
        </p>
        <p>
          Max file size: <strong>20 MB</strong>
        </p>
      </div>
    </div>
  );
}
