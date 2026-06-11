const BASE = "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (res.status === 204) return null;
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}

export const api = {
  getCards: (category) =>
    request(`/cards${category ? `?category=${category}` : ""}`),

  createCard: (data) =>
    request("/cards", { method: "POST", body: JSON.stringify(data) }),

  updateCard: (id, data) =>
    request(`/cards/${id}`, { method: "PUT", body: JSON.stringify(data) }),

  deleteCard: (id) =>
    request(`/cards/${id}`, { method: "DELETE" }),

  getReviewQueue: () => request("/cards/review"),

  submitReview: (id, quality) =>
    request(`/cards/${id}/review`, {
      method: "POST",
      body: JSON.stringify({ quality }),
    }),

  getStats: () => request("/stats"),
};
