from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import Player, RatingHistory
import csv
from io import StringIO
from fastapi.responses import StreamingResponse
from sqlalchemy import text

from top_players import fetch_top_players
from rating_history import get_rating_history

rating_csv_router = APIRouter()

# Endpoint to generate and provide a CSV file with the rating history for the top 50 players
@rating_csv_router.get("/players/rating-history-csv")
async def get_rating_history_csv(db: Session = Depends(get_db)):
    #check if the rating history table is empty
    rating_history = db.query(RatingHistory).first()

    if not rating_history:
        #check if the player table is empty
        player = db.query(Player).first()

        if not player:
            #get the top 50 players
            top_players = fetch_top_players(db)

            #get the rating history for each player
            for player in top_players:
                await get_rating_history(player[0], db)
        
        else:
            #get the rating history for each player
            for player in db.query(Player).all():
                await get_rating_history(player.username, db)
    
    #if rating history is not empty, get the rating history for the top 50 players
    elif rating_history:
        #get the rating history for each player
        for player in db.query(Player).all():
            await get_rating_history(player.username, db)

    #get the rating history for the top 50 players
    rating_history = db.execute(text("""
        SELECT rh.*
        FROM players p
        JOIN rating_history rh ON p.id = rh.player_id
        ORDER BY rh.day_30 DESC
        LIMIT 50
    """)).fetchall()

    #convert the rating history to a list
    rating_history = [list(player) for player in rating_history]

    #create a CSV file
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow(["username", "day_1", "day_2", "day_3", "day_4", "day_5", "day_6", "day_7", "day_8", "day_9", "day_10", "day_11", "day_12", "day_13", "day_14", "day_15", "day_16", "day_17", "day_18", "day_19", "day_20", "day_21", "day_22", "day_23", "day_24", "day_25", "day_26", "day_27", "day_28", "day_29", "day_30"])

    for player in rating_history:
        csv_writer.writerow(player)

    #return the CSV file
    response = StreamingResponse(iter([csv_data.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=rating_history.csv"
    return response