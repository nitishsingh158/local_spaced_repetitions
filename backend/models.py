from typing import Literal, Optional

from pydantic import BaseModel, Field

Category = Literal["python", "sql", "ml", "stats", "product", "ai"]
Language = Literal["python", "sql", "none"]


class CardCreate(BaseModel):
    category: Category
    question: str
    answer: str
    language: Language = "none"


class CardUpdate(BaseModel):
    category: Optional[Category] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    language: Optional[Language] = None


class Card(BaseModel):
    id: str
    category: Category
    question: str
    answer: str
    language: Language
    ease_factor: float
    interval_days: int
    repetitions: int
    next_review: str
    last_reviewed: Optional[str]
    created_at: str
    updated_at: str


class ReviewCard(BaseModel):
    id: str
    category: Category
    question: str
    answer: str
    language: Language


class ReviewSubmit(BaseModel):
    quality: int = Field(..., ge=0, le=5)


class ReviewResponse(BaseModel):
    id: str
    next_review: str
    interval_days: int
    ease_factor: float
    repetitions: int
