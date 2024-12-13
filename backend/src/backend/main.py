from typing import List

from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware

from backend.schemas.auth import UserToken, MailPetition
from backend.schemas.recommend import RecommendedSong
from backend.services.spotify.client import SpotifyClient
from backend.services.spotify.users.app import SpotifyApp
from backend.services.spotify.users.dependencies import get_spotify_app

from src.backend.schemas.recommend import Song
from src.backend.services.antirecommender import AntiRecommenderService

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
    path="/user",
    status_code=200,
)
def add_user_to_spotify_project(
    data: MailPetition, spotify_app: SpotifyApp = Depends(get_spotify_app)
) -> str:
    result = spotify_app.add_user(data.mail)
    if result.is_error:
        raise HTTPException(status_code=404, detail=result.error_value.message)
    return "ok"


@app.post(
    path="/recommend",
    response_model=RecommendedSong,
    status_code=200,
)
def recommend_songs_for_user_with_token(data: UserToken) -> RecommendedSong:
    anti_recommender = AntiRecommenderService(
        data_path="./data/spotify_tracks_dataset.csv"
    )
    spotify = SpotifyClient(access_token=data.access_token)
    songs: List[Song] = spotify.recently_played
    songs_ids = [song.id for song in songs]
    real_ids_in_dataset = anti_recommender.filter_existing_tracks(songs_ids)
    if not real_ids_in_dataset:
        # TODO: Check for something real
        raise HTTPException(status_code=401, detail="No songs to recommend")
        # return RecommendedSong(isRandom=True, fromSongs=songs, recommended=songs[0])
    # return RecommendedSong(isRandom=True, fromSongs=songs, recommended=songs[0])
    # recommended_song_id = anti_recommender.antirecommend(songs_ids)
    raise HTTPException(status_code=403, detail="No songs to recommend")
    # print(recommended_song_id)
    # from_songs = [song for song in songs if song.id in real_ids_in_dataset]
    # return RecommendedSong(
    #     isRandom=False,
    #     fromSongs=from_songs,
    #     recommended=Song(id=recommended_song_id, name="This is the recommended song", image="https://photographylife.com/wp-content/uploads/2014/09/Nikon-D750-Image-Samples-2.jpg"),
    # )
