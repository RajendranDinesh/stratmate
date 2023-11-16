from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
import httpx
from db import get_db
from models import Player, Rating

top_player_router = APIRouter()

def fetch_top_players(db: Session):
    api_url = "https://lichess.org/api/player/top/50/classical"
    response = httpx.get(api_url)

    if response.status_code == 200:
        lichess_data = response.json()["users"]

        for user in lichess_data:
            player_id = user["id"]
            user_name = user["username"]
            rating = user["perfs"]["classical"]["rating"]
            progress = user["perfs"]["classical"]["progress"]

            player = db.query(Player).filter(Player.id == player_id).first()
            if not player:
                player = Player(id=player_id, username=user_name)
                db.add(player)

            rating_record = Rating(player_id=player_id, rating=rating, progress=progress)
            db.add(rating_record)

        db.commit()

        players = db.execute(text("""
            SELECT p.username, r.rating, r.progress
            FROM players p
            JOIN ratings r ON p.id = r.player_id
            ORDER BY r.rating DESC
            LIMIT 50
        """)).fetchall()

        players = [list(player) for player in players]

        return players
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

@top_player_router.get("/top-players", response_model=list)
def get_top_players(db: Session = Depends(get_db)):
    players = db.execute(text("""
        SELECT p.username, r.rating, r.progress
        FROM players p
        JOIN ratings r ON p.id = r.player_id
        ORDER BY r.rating DESC
        LIMIT 50
    """)).fetchall()

    players = [list(player) for player in players]

    if players:
        return players
    else:
        fetch_top_players(db)