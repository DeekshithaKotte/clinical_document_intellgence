import { useMemo, useRef, useState } from "react";
import { uploadFile } from "../api";

function ClinicalDashboard() {
  const [summary, setSummary] = useState(null);
  const [diagnosis, setDiagnosis] = useState(null);
  const [risks, setRisks] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fileName, setFileName] = useState("");
  const [dragActive, setDragActive] = useState(false);

  const inputRef = useRef(null);

  const hasResults = useMemo(
    () => !!summary || !!diagnosis || !!risks,
    [summary, diagnosis, risks]
  );

  async function handleFile(file) {
    if (!file) return;

    setFileName(file.name);
    setLoading(true);
    setError(null);

    try {
      const res = await uploadFile(file);
      setSummary(res.summary || "");
      setDiagnosis(res.diagnosis || "");
      setRisks(res.risks || {});
    } catch (err) {
      setError("Upload failed. Please check backend logs and try again.");
    } finally {
      setLoading(false);
    }
  }

  function onInputChange(e) {
    const file = e.target.files?.[0];
    handleFile(file);
  }

  function onDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    const file = e.dataTransfer.files?.[0];
    handleFile(file);
  }

  function onDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  }

  function onDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <h1 className="title">Clinical RAG Assistant</h1>
          <p className="subtitle">
            Upload a clinical note to generate summary, risks, and differential
            diagnosis.
          </p>
        </div>

        <div className="badge-row">
          <span className="badge">FAISS</span>
          <span className="badge">Local Embeddings</span>
          <span className="badge accent">FastAPI</span>
        </div>
      </header>

      <main className="grid">
        {/* Left column */}
        <section className="card upload-card">
          <h2 className="card-title">Upload Document</h2>

          <div
            className={`dropzone ${dragActive ? "active" : ""}`}
            onClick={() => inputRef.current?.click()}
            onDrop={onDrop}
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
          >
            <input
              ref={inputRef}
              type="file"
              accept=".pdf,.txt"
              onChange={onInputChange}
              hidden
            />

            <div className="dz-inner">
              <div className="dz-icon">⬆️</div>
              <div className="dz-text">
                <p className="dz-head">
                  Drag & drop a PDF/TXT here, or click to browse
                </p>
                <p className="dz-sub">
                  Supported: clinical notes, discharge summaries, guidelines
                </p>
              </div>
            </div>
          </div>

          {fileName && (
            <div className="file-pill">
              <span className="dot" />
              {fileName}
            </div>
          )}

          {loading && (
            <div className="loader">
              <div className="spinner" />
              <div>
                <p className="loader-title">Processing document…</p>
                <p className="loader-sub">
                  Chunking, retrieving context, and generating outputs.
                </p>
              </div>
            </div>
          )}

          {error && <div className="error-box">{error}</div>}

          {!loading && !hasResults && (
            <div className="hint">
              Tip: try uploading your sample note first to validate the pipeline.
            </div>
          )}
        </section>

        {/* Right column */}
        <section className="stack">
          <div className="card">
            <h2 className="card-title">Summary</h2>
            {!summary && <p className="empty">No summary yet.</p>}
            {summary && <pre className="pre">{summary}</pre>}
          </div>

          <div className="card">
            <h2 className="card-title">Risks</h2>
            {!risks && <p className="empty">No risks yet.</p>}
            {risks && (
              <pre className="pre">
                {typeof risks === "string"
                  ? risks
                  : JSON.stringify(risks, null, 2)}
              </pre>
            )}
          </div>

          <div className="card">
            <h2 className="card-title">Differential Diagnosis</h2>
            {!diagnosis && <p className="empty">No diagnosis yet.</p>}
            {diagnosis && <pre className="pre">{diagnosis}</pre>}
          </div>
        </section>
      </main>

      <footer className="footer">
        <span>Clinical RAG Assistant • Local-first inference</span>
      </footer>
    </div>
  );
}

export default ClinicalDashboard;
