# Local Flash Cards

Local spaced repetition.

## Setup

```bash
# Python deps
uv sync

# Frontend deps
cd frontend && npm install && cd ..
```

## Run

Open two terminals:

```bash
# Terminal 1 — backend
uv run uvicorn backend.main:app --reload

# Terminal 2 — frontend
cd frontend && npm run dev
```

Open http://localhost:5173

## Usage

- **Dashboard** — see how many cards are due, start a review session
- **Review** — read the question, use the scratchpad to work through it, reveal the answer, rate yourself (Again / Hard / Good / Easy)
- **Add Card** — create cards with markdown support and optional code blocks
- **Browse** — filter by category, edit or delete cards

## Tests

```bash
uv run pytest backend/tests/ -v
```
