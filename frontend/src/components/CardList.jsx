import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";

const CATEGORIES = ["all", "python", "sql", "ml", "stats", "product", "ai"];

export default function CardList() {
  const [cards, setCards] = useState([]);
  const [filter, setFilter] = useState("all");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    api.getCards(filter === "all" ? null : filter)
      .then(setCards)
      .catch((e) => setError(e.message));
  }, [filter]);

  async function handleDelete(id) {
    if (!confirm("Delete this card?")) return;
    try {
      await api.deleteCard(id);
      setCards((cs) => cs.filter((c) => c.id !== id));
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div className="card-list">
      <header className="list-header">
        <h2>Cards</h2>
        <button onClick={() => navigate("/cards/new")}>Add Card</button>
        <button onClick={() => navigate("/")}>Dashboard</button>
      </header>

      {error && <div className="error">{error}</div>}

      <div className="filter-bar">
        {CATEGORIES.map((c) => (
          <button
            key={c}
            className={filter === c ? "active" : ""}
            onClick={() => setFilter(c)}
          >
            {c}
          </button>
        ))}
      </div>

      {cards.length === 0 ? (
        <p className="empty">No cards found.</p>
      ) : (
        <table className="cards-table">
          <thead>
            <tr>
              <th>Category</th>
              <th>Question</th>
              <th>Next Review</th>
              <th>EF</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {cards.map((card) => (
              <tr key={card.id}>
                <td><span className="category-badge">{card.category}</span></td>
                <td className="question-cell">{card.question.slice(0, 80)}{card.question.length > 80 ? "…" : ""}</td>
                <td>{card.next_review}</td>
                <td>{card.ease_factor.toFixed(2)}</td>
                <td className="actions-cell">
                  <button onClick={() => navigate(`/cards/${card.id}`)}>Edit</button>
                  <button onClick={() => handleDelete(card.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
