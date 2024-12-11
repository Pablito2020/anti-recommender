from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.schemas.auth import UserToken
from backend.schemas.recommend import RecommendedSong
from backend.services.spotify.client import SpotifyClient

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
def root() -> str:
    return "Hello world!"


@app.post(
    path="/recommend",
    response_model=RecommendedSong,
    status_code=200,
)
def recommend_songs_for_user_with_token(data: UserToken) -> RecommendedSong:
    spotify = SpotifyClient(access_token=data.access_token)
    songs = spotify.recently_played
    return RecommendedSong(isRandom=True, fromSongs=songs, recommended=songs[0])
