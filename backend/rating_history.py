from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from db import get_db
from models import Player, RatingHistory

rating_history_router = APIRouter()

#an async function to write the rating history to the database
async def write_rating_history(classical_points, player_id, db):
    #iterate through the list of points and write them to the database

    rating_history = db.query(RatingHistory).filter(RatingHistory.player_id == player_id).first()

    rating_values = {}

    for i in range(len(classical_points)):
        rating_value = classical_points[i][3]
        rating_value = int(classical_points[i][3])
        rating_values[f"day_{i+1}"] = rating_value
    
    #fill the rest of the days with 0
    for i in range(len(classical_points), 30):
        rating_values[f"day_{i+1}"] = 0
    
    if rating_history:
        #update the rating history
        for key, value in rating_values.items():
            setattr(rating_history, key, value)
        db.commit()
    else:
        new_rating_history = RatingHistory(player_id=player_id, **rating_values)
        db.add(new_rating_history)
        db.commit()


# Endpoint to retrieve the 30-day rating history for a specified player
@rating_history_router.get("/player/{username}/rating-history")
async def get_rating_history(username: str, db: Session = Depends(get_db)):
    # Check if the player exists in the 'player' table
    player = db.query(Player).filter(Player.username == username).first()

    if player:
        # Check if the player has a rating history in the 'rating_history' table
        rating_history = db.query(RatingHistory).filter(RatingHistory.player_id == player.id).first()

        if rating_history:
            return rating_history
        
    else:
        async with httpx.AsyncClient() as client:
            api_url = f"https://lichess.org/api/user/{username}"
            response = await client.get(api_url, timeout=5)

            if response.status_code == 200:
                lichess_data = response.json()
                player_id = lichess_data["id"]
                username = lichess_data["username"]

                player = Player(id=player_id, username=username)
                db.add(player)
                db.commit()
            
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)

    async with httpx.AsyncClient() as client:
        api_url = f"https://lichess.org/api/user/{username}/rating-history"
        response = await client.get(api_url)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        lichess_data = response.json()

    classical_points = []

    for category in lichess_data:
        #check if the category is classical
        if category["name"] == 'Classical':

            #reverse the points for the classical category so that the most recent points are at the end of the list
            category["points"] = category["points"][::-1]

            for point in category["points"]:
                #add only the 30 days of data no matter what the date or day is

                if len(classical_points) < 30:
                    classical_points.append(point)
            
            #write the rating history to the database
            await write_rating_history(classical_points, player.id, db)

    return classical_points