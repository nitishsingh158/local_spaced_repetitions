from datetime import date

from fastapi import APIRouter

from backend.database import get_connection

router = APIRouter()

CATEGORIES = ["python", "sql", "ml", "stats", "product", "ai"]


@router.get("/stats")
def get_stats():
    today = date.today().isoformat()
    with get_connection() as conn:
        total_cards = conn.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
        due_today = conn.execute(
            "SELECT COUNT(*) FROM cards WHERE next_review <= ?", (today,)
        ).fetchone()[0]
        avg_ease = conn.execute("SELECT AVG(ease_factor) FROM cards").fetchone()[0]
        reviewed_today = conn.execute(
            "SELECT COUNT(*) FROM cards WHERE last_reviewed = ?", (today,)
        ).fetchone()[0]

        by_category = {}
        for cat in CATEGORIES:
            total = conn.execute(
                "SELECT COUNT(*) FROM cards WHERE category = ?", (cat,)
            ).fetchone()[0]
            due = conn.execute(
                "SELECT COUNT(*) FROM cards WHERE category = ? AND next_review <= ?",
                (cat, today),
            ).fetchone()[0]
            by_category[cat] = {"total": total, "due": due}

    return {
        "total_cards": total_cards,
        "due_today": due_today,
        "by_category": by_category,
        "avg_ease_factor": round(avg_ease, 2) if avg_ease is not None else None,
        "cards_reviewed_today": reviewed_today,
    }
