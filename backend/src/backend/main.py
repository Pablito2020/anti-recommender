from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.backend.schemas.auth import UserToken
from src.backend.schemas.recommend import RecommendedSong
from src.backend.services.spotify import SpotifyService

app = FastAPI(
    title="AntiRecommender API",
    description="Recommend you different songs",
    docs_url="/docs",
    redoc_url="/redoc",
    version="0.1.0",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
def root():
    return "Hello world!"


@app.post("/recommend")
def recommend_songs_for_user_with_token(data: UserToken) -> RecommendedSong:
    spotify = SpotifyService(access_token=data.access_token)
    songs = spotify.recently_played
    return RecommendedSong(isRandom=True, fromSongs=songs, recommended=songs[0])
