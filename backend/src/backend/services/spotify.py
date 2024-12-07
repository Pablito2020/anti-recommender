from typing import List

from pydantic.v1 import ValidationError
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
        try:
            recently_played: RecentlyPlayed = RecentlyPlayed(
                **self.sp.current_user_recently_played()
            )
            songs = []
            for played in recently_played.items:
                songs.append(
                    Song(
                        name=played.track.name,
                        image=None
                        if len(played.track.album.images) == 0
                        else played.track.album.images[0].url,
                    )
                )
            return songs
        except ValidationError:
            print("Validation error...")
            return []
