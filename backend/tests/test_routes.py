import pytest
from fastapi.testclient import TestClient

import backend.database as db_module
from backend.database import init_db
from backend.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    monkeypatch.setattr(db_module, "DB_PATH", db_file)
    init_db()
    with TestClient(app) as c:
        yield c


# --- cards CRUD ---

def test_create_card(client):
    r = client.post("/cards", json={
        "category": "python",
        "question": "What is a decorator?",
        "answer": "A function that wraps another function.",
        "language": "python",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["category"] == "python"
    assert "id" in data
    assert data["ease_factor"] == 2.5
    assert data["repetitions"] == 0


def test_list_cards_empty(client):
    r = client.get("/cards")
    assert r.status_code == 200
    assert r.json() == []


def test_list_cards(client):
    client.post("/cards", json={
        "category": "sql",
        "question": "What is a JOIN?",
        "answer": "Combines rows from two tables.",
        "language": "sql",
    })
    r = client.get("/cards")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_list_cards_category_filter(client):
    client.post("/cards", json={"category": "python", "question": "Q1", "answer": "A1"})
    client.post("/cards", json={"category": "sql", "question": "Q2", "answer": "A2"})
    r = client.get("/cards?category=python")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["category"] == "python"


def test_update_card(client):
    created = client.post("/cards", json={
        "category": "ml",
        "question": "What is overfitting?",
        "answer": "Model too complex.",
    }).json()
    r = client.put(f"/cards/{created['id']}", json={"question": "Define overfitting."})
    assert r.status_code == 200
    assert r.json()["question"] == "Define overfitting."
    assert r.json()["ease_factor"] == created["ease_factor"]


def test_update_card_not_found(client):
    r = client.put("/cards/nonexistent", json={"question": "X"})
    assert r.status_code == 404


def test_delete_card(client):
    created = client.post("/cards", json={
        "category": "stats",
        "question": "What is p-value?",
        "answer": "Probability of observing result under null.",
    }).json()
    r = client.delete(f"/cards/{created['id']}")
    assert r.status_code == 204
    assert client.get("/cards").json() == []


def test_delete_card_not_found(client):
    r = client.delete("/cards/nonexistent")
    assert r.status_code == 404


# --- review queue ---

def test_review_queue_returns_due_cards(client):
    client.post("/cards", json={
        "category": "python",
        "question": "Q",
        "answer": "A",
    })
    r = client.get("/cards/review")
    assert r.status_code == 200
    assert len(r.json()) == 1
    card = r.json()[0]
    assert set(card.keys()) == {"id", "category", "question", "answer", "language"}


def test_review_queue_excludes_future_cards(client):
    # Create a card then push its next_review into the future via a review
    created = client.post("/cards", json={
        "category": "python",
        "question": "Q",
        "answer": "A",
    }).json()
    client.post(f"/cards/{created['id']}/review", json={"quality": 5})
    r = client.get("/cards/review")
    assert r.status_code == 200
    assert r.json() == []


# --- submit review ---

def test_submit_review(client):
    created = client.post("/cards", json={
        "category": "ai",
        "question": "What is a transformer?",
        "answer": "Attention-based architecture.",
    }).json()
    r = client.post(f"/cards/{created['id']}/review", json={"quality": 4})
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == created["id"]
    assert data["repetitions"] == 1
    assert data["interval_days"] == 1
    assert "next_review" in data
    assert "ease_factor" in data


def test_submit_review_not_found(client):
    r = client.post("/cards/nonexistent/review", json={"quality": 4})
    assert r.status_code == 404


# --- stats ---

def test_stats_empty(client):
    r = client.get("/stats")
    assert r.status_code == 200
    data = r.json()
    assert data["total_cards"] == 0
    assert data["due_today"] == 0
    assert data["avg_ease_factor"] is None
    assert data["cards_reviewed_today"] == 0
    assert set(data["by_category"].keys()) == {
        "python", "sql", "ml", "stats", "product", "ai"
    }


def test_stats_with_cards(client):
    client.post("/cards", json={"category": "python", "question": "Q", "answer": "A"})
    r = client.get("/stats")
    assert r.status_code == 200
    data = r.json()
    assert data["total_cards"] == 1
    assert data["due_today"] == 1
    assert data["by_category"]["python"]["total"] == 1
    assert data["by_category"]["python"]["due"] == 1
