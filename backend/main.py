from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import uvicorn

from top_players import top_player_router
from rating_history import rating_history_router
from rating_history_csv import rating_csv_router
from user import user_router
from utils import JWTBearer

app = FastAPI()

@app.get('/')
async def health_check():
    return {'message': 'OK'}

app.include_router(router=top_player_router, prefix='/api', dependencies=[Depends(JWTBearer())])
app.include_router(router=rating_history_router, prefix='/api', dependencies=[Depends(JWTBearer())])
app.include_router(router=rating_csv_router, prefix='/api', dependencies=[Depends(JWTBearer())])
app.include_router(router=user_router, prefix='/api')

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title = "lichess custom API",
        version = "0.0.1",
        description = "This API provides the top 50 players and their rating history for the last 30 days.",
        routes = app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_level='debug',
        reload=True
    )