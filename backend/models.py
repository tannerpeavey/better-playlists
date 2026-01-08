from pydantic import BaseModel
from typing import List, Optional

class Song(BaseModel):
    spotify_id: str
    title: str
    artist: str
    tags: Optional[List[str]] = []

    # Emotional axes (0-1 continuous)
    energy: Optional[float] = None
    valence: Optional[float] = None
    danceability: Optional[float] = None

class Playlist(BaseModel):
    name: str
    songs: List[Song]

class EmotionUpdate(BaseModel):
    energy: Optional[float] = None
    valence: Optional[float] = None
    danceability: Optional[float] = None