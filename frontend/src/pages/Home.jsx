import { Link } from "react-router-dom";
import "./Home.css";

function Home() {
  return (
    <div className="home-container">
      <div className="home-content">
        <div className="logo-area">
          <span className="logo-icon">🔮</span>
          <h1 className="app-title">ArcaneQuiz</h1>
          <p className="subtitle">Where Knowledge Meets Sorcery</p>
        </div>
        <p className="home-description">
          Upload your ancient scrolls (PDF, DOCX, TXT) and let the magical AI
          forge questions worthy of a wizard's examination.
        </p>
        <Link to="/upload" className="enter-btn">
          <span className="btn-icon">📜</span>
          Enter the Forge
        </Link>
        <div className="features">
          <div className="feature-item">
            <span className="feature-icon">✨</span>
            <span>Multiple AI Providers</span>
          </div>
          <div className="feature-item">
            <span className="feature-icon">📊</span>
            <span>PDF Export with Metadata</span>
          </div>
          <div className="feature-item">
            <span className="feature-icon">🔍</span>
            <span>Review & Search Questions</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
