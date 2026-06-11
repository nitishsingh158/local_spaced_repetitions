import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../api";

const CATEGORIES = ["python", "sql", "ml", "stats", "product", "ai"];
const LANGUAGES = ["none", "python", "sql"];

const EMPTY = { category: "python", question: "", answer: "", language: "none" };

export default function CardForm() {
  const { id } = useParams();
  const isEdit = Boolean(id);
  const navigate = useNavigate();

  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!isEdit) return;
    api.getCards()
      .then((cards) => {
        const card = cards.find((c) => c.id === id);
        if (!card) { setError("Card not found"); return; }
        setForm({
          category: card.category,
          question: card.question,
          answer: card.answer,
          language: card.language,
        });
      })
      .catch((e) => setError(e.message));
  }, [id, isEdit]);

  function set(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      if (isEdit) {
        await api.updateCard(id, form);
      } else {
        await api.createCard(form);
      }
      navigate("/cards");
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="card-form">
      <h2>{isEdit ? "Edit Card" : "New Card"}</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <label>
          Category
          <select value={form.category} onChange={(e) => set("category", e.target.value)}>
            {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
        </label>

        <label>
          Language
          <select value={form.language} onChange={(e) => set("language", e.target.value)}>
            {LANGUAGES.map((l) => <option key={l} value={l}>{l}</option>)}
          </select>
        </label>

        <label>
          Question
          <textarea
            rows={5}
            value={form.question}
            onChange={(e) => set("question", e.target.value)}
            required
          />
        </label>

        <label>
          Answer
          <textarea
            rows={8}
            value={form.answer}
            onChange={(e) => set("answer", e.target.value)}
            required
          />
        </label>

        <div className="form-actions">
          <button type="button" onClick={() => navigate("/cards")}>Cancel</button>
          <button type="submit" disabled={saving}>
            {saving ? "Saving..." : isEdit ? "Save Changes" : "Create Card"}
          </button>
        </div>
      </form>
    </div>
  );
}
