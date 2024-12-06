from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from spotipy import Spotify
from spotipy.exceptions import SpotifyException
from .models import UserToken

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
def recommend_songs_for_user_with_token(data: UserToken):
    try:
        sp = Spotify(auth=data.access_token)
        print("User playlists:")
        print(sp.current_user_playlists())
        print("Recently played:")
        print(sp.current_user_recently_played())
        print("Top tracks:")
        print(sp.current_user_top_tracks())
        return sp.current_user_playlists()
    except SpotifyException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error loading your spotify profile... Error message: ${e.reason}",
        )
