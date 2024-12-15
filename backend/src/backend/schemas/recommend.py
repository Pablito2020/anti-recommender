from typing import List

from pydantic import BaseModel


class Song(BaseModel):
    id: str
    name: str
    image: str | None = None


class RecommendedSong(BaseModel):
    isRandom: bool
    fromSongs: List[Song]
    recommended: Song
