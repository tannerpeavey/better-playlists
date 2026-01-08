from fastapi import APIRouter, Query
from models import Song, Playlist
from typing import List
from spotify_client import get_spotify_token, get_audio_features
import requests


router = APIRouter()



# Temporary in-memory store
# songs_db: List[Song] = []
# Hardcoded in-memory songs for testing
songs_db: list[Song] = [
    Song(
        spotify_id="3KkXRkHbMCARz0aVfEt68P",
        title="Imagine",
        artist="John Lennon",
        energy=0.33,
        valence=0.67,
        danceability=0.52,
        tags=[]
    ),
    Song(
        spotify_id="7GhIk7Il098yCjg4BQjzvb",
        title="Billie Jean",
        artist="Michael Jackson",
        energy=0.85,
        valence=0.73,
        danceability=0.88,
        tags=[]
    ),
    Song(
        spotify_id="1AhDOtG9vPSOmsWgNW0BEY",
        title="Bohemian Rhapsody",
        artist="Queen",
        energy=0.45,
        valence=0.40,
        danceability=0.35,
        tags=[]
    ),
    Song(
        spotify_id="4VqPOruhp5EdPBeR92t6lQ",
        title="Blinding Lights",
        artist="The Weeknd",
        energy=0.80,
        valence=0.91,
        danceability=0.75,
        tags=[]
    ),
    Song(
        spotify_id="5ChkMS8OtdzJeqyybCc9R5",
        title="Sweet Child O’Mine",
        artist="Guns N’ Roses",
        energy=0.75,
        valence=0.60,
        danceability=0.65,
        tags=[]
    )
]
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
# @router.get("/generate-playlist")
# def generate_playlist():
#     # TODO: implement playlist generation logic
#     return {"message": "Playlist generation coming soon!"}

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
    # Create the song object
    song = Song(spotify_id=spotify_id, title=title, artist=artist)
    
    # Get a Spotify token
    token = get_spotify_token()
    
    # Fetch audio features from Spotify
    features = get_audio_features(song.spotify_id, token)
    
    # Assign features to the song
    song.energy = features.get("energy")
    song.valence = features.get("valence")
    song.danceability = features.get("danceability")
    
    # Save to in-memory database
    songs_db.append(song)
    
    return {"message": "Song added with Spotify audio features!", "song": song}

@router.get("/generate-playlist")
def generate_playlist(
    target_energy: float = Query(..., ge=0.0, le=1.0),
    target_valence: float = Query(..., ge=0.0, le=1.0),
    target_danceability: float = Query(..., ge=0.0, le=1.0),
    limit: int = 10
):
    # Score each song
    scored_songs = []
    for song in songs_db:
        # Skip songs missing any features
        if song.energy is None or song.valence is None or song.danceability is None:
            continue
        
        distance = (
            abs(song.energy - target_energy) +
            abs(song.valence - target_valence) +
            abs(song.danceability - target_danceability)
        )
        scored_songs.append((distance, song))
    
    # Sort by closest match
    scored_songs.sort(key=lambda x: x[0])
    
    # Take top N
    top_songs = [song for _, song in scored_songs[:limit]]
    
    # Return as a playlist
    playlist = Playlist(name="Generated Playlist", songs=top_songs)
    return {"playlist": playlist}