from fastapi import FastAPI
from dotenv import load_dotenv
import os
from routes import router

# Load environment variables from .env
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Create FastAPI app
app = FastAPI(title="Better Playlists Backend")

# Include routes
app.include_router(router)

# Simple test print to verify credentials load
print("Better Playlists loaded. Spotify Client ID:", CLIENT_ID)
