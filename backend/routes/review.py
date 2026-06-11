from datetime import date

from fastapi import APIRouter, HTTPException

from backend.database import get_connection
from backend.models import ReviewCard, ReviewResponse, ReviewSubmit
from backend.sm2 import sm2

router = APIRouter()


@router.get("/cards/review", response_model=list[ReviewCard])
def get_review_queue():
    today = date.today().isoformat()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, category, question, answer, language FROM cards WHERE next_review <= ? ORDER BY ease_factor ASC",
            (today,),
        ).fetchall()
    return [ReviewCard(**dict(r)) for r in rows]


@router.post("/cards/{card_id}/review", response_model=ReviewResponse)
def submit_review(card_id: str, body: ReviewSubmit):
    today = date.today().isoformat()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT ease_factor, interval_days, repetitions FROM cards WHERE id = ?",
            (card_id,),
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Card not found")

        result = sm2(
            quality=body.quality,
            ease_factor=row["ease_factor"],
            interval_days=row["interval_days"],
            repetitions=row["repetitions"],
            today=today,
        )

        conn.execute(
            """
            UPDATE cards
            SET ease_factor = ?, interval_days = ?, repetitions = ?,
                next_review = ?, last_reviewed = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                result.ease_factor,
                result.interval_days,
                result.repetitions,
                result.next_review,
                today,
                today,
                card_id,
            ),
        )
        conn.commit()

    return ReviewResponse(
        id=card_id,
        next_review=result.next_review,
        interval_days=result.interval_days,
        ease_factor=result.ease_factor,
        repetitions=result.repetitions,
    )
