from fastapi import APIRouter
from models import Song, Playlist
from typing import List
from spotify_client import get_spotify_token
import requests


router = APIRouter()



# Temporary in-memory store
songs_db: List[Song] = []
playlists_db: List[Playlist] = []

# Root route
@router.get("/")
def root():
    return {"message": "Welcome to Better Playlists!"}

# Add a song
@router.post("/songs")
def add_song(song: Song):
    songs_db.append(song)
    return {"message": "Song added to Better Playlists!", "song": song}

# List all songs
@router.get("/songs")
def list_songs():
    return {"songs": songs_db}

# Tag a song (example: add tags)
@router.post("/songs/{spotify_id}/tags")
def add_tags(spotify_id: str, tags: List[str]):
    for song in songs_db:
        if song.spotify_id == spotify_id:
            if song.tags is None:
                song.tags = []
            song.tags.extend(tags)
            return {"message": "Tags added!", "song": song}
    return {"error": "Song not found"}

# Generate a playlist (stub for now)
@router.get("/generate-playlist")
def generate_playlist():
    # TODO: implement playlist generation logic
    return {"message": "Playlist generation coming soon!"}

@router.get("/search")
def search_songs(query: str):
    token = get_spotify_token()
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": query,   # the search query string
        "type": "track",
        "limit": 5    # top 5 results
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


@router.post("/add-song")
def add_song(spotify_id: str, title: str, artist: str):
    song = Song(spotify_id=spotify_id, title=title, artist=artist)
    songs_db.append(song)
    return {"message": "Song added!", "song": song}