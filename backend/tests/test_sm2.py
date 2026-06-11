import pytest
from backend.sm2 import sm2, ReviewResult

TODAY = "2026-06-05"


# --- quality 0-5: basic output shape and EF direction ---

@pytest.mark.parametrize("quality", [0, 1, 2, 3, 4, 5])
def test_returns_review_result(quality):
    r = sm2(quality, 2.5, 0, 0, TODAY)
    assert isinstance(r, ReviewResult)
    assert r.ease_factor >= 1.3
    assert r.interval_days >= 1
    assert r.repetitions >= 0
    assert r.next_review > TODAY


@pytest.mark.parametrize("quality,expected_direction", [
    (5, "up"),    # EF increases
    (4, "same"),  # EF unchanged (0.1 - 0.08 - 0.02 = 0)
    (3, "down"),  # EF decreases
    (2, "down"),
    (1, "down"),
    (0, "down"),
])
def test_ef_direction(quality, expected_direction):
    initial_ef = 2.5
    r = sm2(quality, initial_ef, 0, 0, TODAY)
    if expected_direction == "up":
        assert r.ease_factor > initial_ef
    elif expected_direction == "same":
        assert abs(r.ease_factor - initial_ef) < 1e-9
    else:
        assert r.ease_factor < initial_ef


# --- EF floor ---

def test_ef_floor_at_1_3():
    # Drive EF down with repeated quality=0 from minimum
    r = sm2(0, 1.3, 1, 0, TODAY)
    assert r.ease_factor == 1.3


def test_ef_never_below_1_3():
    ef = 2.5
    interval, reps = 0, 0
    for _ in range(20):
        r = sm2(0, ef, interval, reps, TODAY)
        ef, interval, reps = r.ease_factor, r.interval_days, r.repetitions
    assert ef >= 1.3


# --- interval progression across multiple successful reviews ---

def test_interval_progression_successful_reviews():
    today = TODAY
    ef, interval, reps = 2.5, 0, 0

    r1 = sm2(4, ef, interval, reps, today)
    assert r1.repetitions == 1
    assert r1.interval_days == 1

    r2 = sm2(4, r1.ease_factor, r1.interval_days, r1.repetitions, today)
    assert r2.repetitions == 2
    assert r2.interval_days == 6

    r3 = sm2(4, r2.ease_factor, r2.interval_days, r2.repetitions, today)
    assert r3.repetitions == 3
    assert r3.interval_days == round(6 * r2.ease_factor)


# --- failed recall: reps and interval reset, EF NOT reset ---

def test_failed_recall_resets_reps_and_interval():
    r = sm2(1, 2.5, 10, 5, TODAY)
    assert r.repetitions == 0
    assert r.interval_days == 1


def test_failed_recall_does_not_reset_ef():
    initial_ef = 2.2
    r = sm2(1, initial_ef, 10, 5, TODAY)
    # EF should have changed (decreased) but not been reset to 2.5
    assert r.ease_factor != 2.5
    assert r.ease_factor < initial_ef  # it drops, not resets


@pytest.mark.parametrize("quality", [0, 1, 2])
def test_all_failing_qualities_reset_reps(quality):
    r = sm2(quality, 2.5, 15, 4, TODAY)
    assert r.repetitions == 0
    assert r.interval_days == 1


@pytest.mark.parametrize("quality", [3, 4, 5])
def test_all_passing_qualities_increment_reps(quality):
    r = sm2(quality, 2.5, 0, 0, TODAY)
    assert r.repetitions == 1


# --- next_review date is correct ---

def test_next_review_offset():
    r = sm2(4, 2.5, 0, 0, TODAY)
    assert r.next_review == "2026-06-06"  # interval=1, today+1

    r2 = sm2(4, r.ease_factor, r.interval_days, r.repetitions, TODAY)
    assert r2.next_review == "2026-06-11"  # interval=6, today+6
