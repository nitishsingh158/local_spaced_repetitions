from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from backend.database import get_connection
from backend.models import Card, CardCreate, CardUpdate

router = APIRouter()


def _row_to_card(row) -> Card:
    return Card(**dict(row))


@router.get("/cards", response_model=list[Card])
def list_cards(category: Optional[str] = None):
    with get_connection() as conn:
        if category:
            rows = conn.execute(
                "SELECT * FROM cards WHERE category = ?", (category,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM cards").fetchall()
    return [_row_to_card(r) for r in rows]


@router.post("/cards", response_model=Card, status_code=201)
def create_card(body: CardCreate):
    now = datetime.now(timezone.utc).isoformat()
    from datetime import date

    card_id = str(uuid4())
    next_review = date.today().isoformat()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO cards
                (id, category, question, answer, language,
                 ease_factor, interval_days, repetitions,
                 next_review, last_reviewed, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 2.5, 0, 0, ?, NULL, ?, ?)
            """,
            (
                card_id,
                body.category,
                body.question,
                body.answer,
                body.language,
                next_review,
                now,
                now,
            ),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM cards WHERE id = ?", (card_id,)
        ).fetchone()
    return _row_to_card(row)


@router.put("/cards/{card_id}", response_model=Card)
def update_card(card_id: str, body: CardUpdate):
    fields = body.model_dump(exclude_none=True)
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    now = datetime.now(timezone.utc).isoformat()
    fields["updated_at"] = now

    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [card_id]

    with get_connection() as conn:
        result = conn.execute(
            f"UPDATE cards SET {set_clause} WHERE id = ?", values
        )
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Card not found")
        row = conn.execute(
            "SELECT * FROM cards WHERE id = ?", (card_id,)
        ).fetchone()
    return _row_to_card(row)


@router.delete("/cards/{card_id}", status_code=204)
def delete_card(card_id: str):
    with get_connection() as conn:
        result = conn.execute("DELETE FROM cards WHERE id = ?", (card_id,))
        conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Card not found")
    return Response(status_code=204)
