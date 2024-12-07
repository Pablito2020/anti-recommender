from typing import List, Optional, Dict
from pydantic import BaseModel, HttpUrl

class ExternalUrls(BaseModel):
    spotify: HttpUrl

class Image(BaseModel):
    height: int
    url: HttpUrl
    width: int

class Artist(BaseModel):
    external_urls: ExternalUrls
    href: HttpUrl
    id: str
    name: str
    type: str
    uri: str

class Album(BaseModel):
    album_type: str
    artists: List[Artist]
    available_markets: List[str]
    external_urls: ExternalUrls
    href: HttpUrl
    id: str
    images: List[Image]
    name: str
    release_date: str
    release_date_precision: str
    total_tracks: int
    type: str
    uri: str

class ExternalIds(BaseModel):
    isrc: str

class Track(BaseModel):
    album: Album
    artists: List[Artist]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: ExternalIds
    external_urls: ExternalUrls
    href: HttpUrl
    id: str
    is_local: bool
    name: str
    popularity: int
    preview_url: Optional[HttpUrl]
    track_number: int
    type: str
    uri: str

class PlayedItem(BaseModel):
    track: Track
    played_at: str
    context: Optional[dict]

class Cursors(BaseModel):
    after: str
    before: str

class RecentlyPlayed(BaseModel):
    items: List[PlayedItem]
    next: Optional[HttpUrl]
    cursors: Cursors
    limit: int
    href: HttpUrl
