from typing import List

from spotipy import Spotify, SpotifyException
from starlette.exceptions import HTTPException

from src.backend.schemas.recommend import Song
from src.backend.schemas.spotify import RecentlyPlayed


class SpotifyService:
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
        recently_played: RecentlyPlayed = RecentlyPlayed(
            **self.sp.current_user_recently_played()
        )
        songs = []
        for played in recently_played.items:
            song = Song(
                name=played.track.name,
                image=None
                if len(played.track.album.images) == 0
                else played.track.album.images[0].url,
            )
            songs.append(song)
        return songs
