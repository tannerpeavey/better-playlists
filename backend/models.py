from pydantic import BaseModel
from typing import List, Optional

class Song(BaseModel):
    spotify_id: str
    title: str
    artist: str
    tags: Optional[List[str]] = []

class Playlist(BaseModel):
    name: str
    songs: List[Song]
