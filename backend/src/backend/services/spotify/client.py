from typing import List

from spotipy import Spotify, SpotifyException
from starlette.exceptions import HTTPException

from backend.schemas.recommend import Song
from backend.schemas.spotify import RecentlyPlayed


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
