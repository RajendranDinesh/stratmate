import pytest
from fastapi.testclient import TestClient
from main import app 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from models import Player

from db import get_db

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency override for get_db
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_get_rating_history_existing_user():
    # Add a test user to the database
    db = TestingSessionLocal()
    test_user = Player(id="testuser", username="Test User")
    db.add(test_user)
    db.commit()

    # Test the endpoint
    response = client.get("/player/testuser/rating-history")
    assert response.status_code == 200
    assert "points" in response.json()

def test_get_rating_history_non_existing_user():
    response = client.get("/player/nonexistentuser/rating-history")
    assert response.status_code == 404

def test_get_rating_history_csv():
    response = client.get("/players/rating-history-csv")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/csv"

    # Optional: Check the content of the CSV
    content = response.content.decode()
    assert "username,day_1,day_2,day_3,day_4,day_5,day_6,day_7,day_8,day_9,day_10,day_11,day_12,day_13,day_14,day_15,day_16,day_17,day_18,day_19,day_20,day_21,day_22,day_23,day_24,day_25,day_26,day_27,day_28,day_29,day_30" in content

def test_get_top_players():
    # Add some test players to the database
    db = TestingSessionLocal()
    test_user1 = Player(id="testuser1", username="Test User 1")
    test_user2 = Player(id="testuser2", username="Test User 2")
    db.add(test_user1)
    db.add(test_user2)
    db.commit()

    # Test the endpoint
    response = client.get("/top-players")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # Optional: Check the content of the response
    players = response.json()
    assert len(players) > 0
    assert "Test User 1" in [player[0] for player in players]
    assert "Test User 2" in [player[0] for player in players]