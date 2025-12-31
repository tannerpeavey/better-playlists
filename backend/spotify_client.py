import os
from dotenv import load_dotenv
import requests
from base64 import b64encode

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

def get_spotify_token():
    """
    Get an OAuth token from Spotify using Client Credentials flow.
    """
    url = "https://accounts.spotify.com/api/token"
    auth_header = b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    token = response.json().get("access_token")
    return token
