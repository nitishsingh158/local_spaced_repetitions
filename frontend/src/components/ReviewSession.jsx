import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";
import MarkdownRender from "./MarkdownRender";
import Scratchpad from "./Scratchpad";

const QUALITY = [
  { label: "Again", value: 1 },
  { label: "Hard", value: 2 },
  { label: "Good", value: 4 },
  { label: "Easy", value: 5 },
];

export default function ReviewSession() {
  const [queue, setQueue] = useState([]);
  const [index, setIndex] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [done, setDone] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    api.getReviewQueue()
      .then((cards) => {
        setQueue(cards);
        if (cards.length === 0) setDone(true);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  async function handleQuality(quality) {
    const card = queue[index];
    try {
      await api.submitReview(card.id, quality);
    } catch (e) {
      setError(e.message);
      return;
    }
    const next = index + 1;
    if (next >= queue.length) {
      setDone(true);
    } else {
      setIndex(next);
      setRevealed(false);
    }
  }

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (done) {
    return (
      <div className="review-done">
        <h2>All done!</h2>
        <button onClick={() => navigate("/")}>Back to Dashboard</button>
      </div>
    );
  }

  const card = queue[index];

  return (
    <div className="review-session">
      <div className="review-header">
        <span className="category-badge">{card.category}</span>
        <span className="progress">Card {index + 1} of {queue.length}</span>
      </div>

      <div className="review-question">
        <MarkdownRender>{card.question}</MarkdownRender>
      </div>

      <Scratchpad language={card.language} resetKey={card.id} />

      {!revealed ? (
        <button className="reveal-btn" onClick={() => setRevealed(true)}>
          Reveal Answer
        </button>
      ) : (
        <>
          <div className="review-answer">
            <MarkdownRender>{card.answer}</MarkdownRender>
          </div>
          <div className="quality-buttons">
            {QUALITY.map(({ label, value }) => (
              <button
                key={value}
                className={`quality-btn quality-${label.toLowerCase()}`}
                onClick={() => handleQuality(value)}
              >
                {label}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
