from typing import List, Optional

from pydantic import BaseModel


class Song(BaseModel):
    name: str
    image: Optional[str]


class RecommendedSong(BaseModel):
    isRandom: bool
    fromSongs: List[Song]
    recommended: Song
