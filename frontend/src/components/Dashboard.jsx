import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    api.getStats()
      .then(setStats)
      .catch((e) => setError(e.message));
  }, []);

  if (error) return <div className="error">Error: {error}</div>;
  if (!stats) return <div className="loading">Loading...</div>;

  const categories = Object.entries(stats.by_category);

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>DS Prep</h1>
        <nav>
          <button onClick={() => navigate("/cards")}>Browse Cards</button>
          <button onClick={() => navigate("/cards/new")}>Add Card</button>
        </nav>
      </header>

      <section className="due-banner">
        <span className="due-count">{stats.due_today}</span>
        <span className="due-label">cards due today</span>
        <button
          className="start-review"
          disabled={stats.due_today === 0}
          onClick={() => navigate("/review")}
        >
          Start Review
        </button>
      </section>

      <section className="category-grid">
        {categories.map(([cat, { total, due }]) => (
          <div key={cat} className="category-card">
            <span className="category-name">{cat}</span>
            <span className="category-stats">
              {due} due / {total} total
            </span>
          </div>
        ))}
      </section>

      <section className="summary">
        <div>Total cards: <strong>{stats.total_cards}</strong></div>
        <div>Avg ease: <strong>{stats.avg_ease_factor ?? "—"}</strong></div>
        <div>Reviewed today: <strong>{stats.cards_reviewed_today}</strong></div>
      </section>
    </div>
  );
}
