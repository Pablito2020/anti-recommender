from typing import List

from spotipy import Spotify, SpotifyException
from starlette.exceptions import HTTPException

from backend.schemas.recommend import Song
from backend.schemas.spotify import RecentlyPlayed

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
            songs = []
            for played in recently_played.items:
                song = Song(
                    id=played.track.id,
                    name=played.track.name,
                    image=None
                    if len(played.track.album.images) == 0
                    else played.track.album.images[0].url,
                )
                songs.append(song)
            return songs
        except SpotifyException:
            return []

    def get_song_from_id(self, song_id: str) -> Song | None:
        try:
            spotify_track = self.sp.track(track_id=song_id)
            track = Track(**spotify_track)
            return Song(
                id=track.id,
                name=track.name,
                image=track.album.images[0].url
                if len(track.album.images) > 0
                else None,
            )
        except SpotifyException:
            return None
