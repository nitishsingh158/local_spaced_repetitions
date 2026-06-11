from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class ReviewResult:
    ease_factor: float
    interval_days: int
    repetitions: int
    next_review: str  # ISO date string YYYY-MM-DD


def sm2(
    quality: int,
    ease_factor: float,
    interval_days: int,
    repetitions: int,
    today: str,
) -> ReviewResult:
    if quality >= 3:
        repetitions += 1
        if repetitions == 1:
            interval_days = 1
        elif repetitions == 2:
            interval_days = 6
        else:
            interval_days = round(interval_days * ease_factor)
    else:
        repetitions = 0
        interval_days = 1

    ease_factor = max(
        1.3,
        ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02),
    )

    next_review = (date.fromisoformat(today) + timedelta(days=interval_days)).isoformat()

    return ReviewResult(
        ease_factor=ease_factor,
        interval_days=interval_days,
        repetitions=repetitions,
        next_review=next_review,
    )
