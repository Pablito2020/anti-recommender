from typing import List

from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware

from src.backend.schemas.auth import UserToken, MailPetition
from src.backend.schemas.recommend import RecommendedSong
from src.backend.services.spotify.client import SpotifyClient
from src.backend.services.spotify.users.app import (
    SpotifyApp,
    MailError,
    FetchUsersError,
    DuplicatedUserInDatabaseError,
    DeletingUserError,
    CreatingUserError,
    TokenExpired,
)
from src.backend.services.spotify.users.dependencies import get_spotify_app

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
        match result.error_value:
            case MailError():
                raise HTTPException(status_code=400, detail=result.error_value.message)
            case DuplicatedUserInDatabaseError():
                raise HTTPException(
                    status_code=409,
                    detail="You're saved twice on our database. Please contact the admins",
                )
            case (
                FetchUsersError()
                | DeletingUserError()
                | CreatingUserError()
                | TokenExpired()
            ):
                raise HTTPException(status_code=502, detail=result.error_value.message)
            case _:
                raise HTTPException(status_code=500, detail=result.error_value.message)
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
    is_random = not real_ids_in_dataset
    track_id = (
        anti_recommender.get_random_track()
        if is_random
        else anti_recommender.antirecommend(songs_ids)
    )
    song = spotify.get_song_from_id(song_id=track_id)
    from_songs = [song for song in songs if song.id in real_ids_in_dataset]
    if song is None:
        could_not_fetch_name_and_image = Song(
            id=track_id, name="Couldn't fetch name, click to go to the song"
        )
        return RecommendedSong(
            isRandom=is_random,
            fromSongs=from_songs,
            recommended=could_not_fetch_name_and_image,
        )
    return RecommendedSong(isRandom=is_random, fromSongs=from_songs, recommended=song)
