from typing import List

from pydantic import ValidationError
from spotipy import Spotify, SpotifyException
from starlette.exceptions import HTTPException

from src.backend.schemas.recommend import Song
from src.backend.schemas.spotify import RecentlyPlayed

from src.backend.schemas.spotify import Track


class SpotifyClient:
    def __init__(self, access_token: str):
        try:
            self.sp = Spotify(auth=access_token)
        except SpotifyException as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error loading your spotify profile... Error message: ${e.reason}",
            )

    @property
    def recently_played(self) -> List[Song]:
        try:
            recently_played: RecentlyPlayed = RecentlyPlayed(
                **self.sp.current_user_recently_played()
            )
            return [
                SpotifyClient.__to_song(played.track)
                for played in recently_played.items
            ]
        except SpotifyException:
            return []

    def get_song_from_id(self, song_id: str) -> Song | None:
        try:
            spotify_track = self.sp.track(track_id=song_id)
            track = Track(**spotify_track)
            return SpotifyClient.__to_song(track)
        except SpotifyException | ValidationError | ValueError:
            return None

    @staticmethod
    def __to_song(track: Track) -> Song:
        return Song(
            id=track.id, name=track.name, image=SpotifyClient.__get_image_url(track)
        )

    @staticmethod
    def __get_image_url(track: Track) -> str | None:
        if len(track.album.images) > 0:
            return track.album.images[0].url
        return None
