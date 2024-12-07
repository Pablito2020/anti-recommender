from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class Song(BaseModel):
    name: str
    image: Optional[HttpUrl]

class RecommendedSong(BaseModel):
    isRandom: bool
    fromSongs: Optional[List[Song]]
    recommended: Song

