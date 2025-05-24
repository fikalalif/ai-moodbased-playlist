# import os
# from spotipy.oauth2 import SpotifyOAuth
# from spotipy import Spotify
# from dotenv import load_dotenv

# load_dotenv()

# MOOD_TO_GENRE = {
#     "happy": "party",
#     "sad": "sad",
#     "angry": "rock",
#     "surprise": "edm",
#     "neutral": "chill",
#     "positive": "happy",
#     "negative": "sad"
# }

# # OPTIONAL: Hapus inisialisasi `sp` di sini
# # Karena `sp` harus dibuat di `app.py` setelah user login
# # Jadi hapus ini:
# # sp = Spotify(...)

# def get_playlist(mood, sp):
#     try:
#         search_results = sp.search(q=mood + " mood", type='playlist', limit=1)
#         playlists = search_results.get('playlists', {}).get('items', [])
#         if playlists:
#             return playlists[0]['external_urls']['spotify']
#         else:
#             print(f"[WARN] No playlist found for mood: {mood}")
#             return None
#     except Exception as e:
#         print(f"[ERROR] Failed to fetch playlist: {e}")
#         return None

import os
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
from dotenv import load_dotenv

load_dotenv()

MOOD_TO_GENRE = {
    "happy": "party",
    "sad": "sad",
    "angry": "rock",
    "surprise": "edm",
    "neutral": "chill",
    "positive": "happy",
    "negative": "sad"
}

def create_spotify_client():
    return Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-read-private"
    ))

def get_playlist(mood, sp):
    genre = MOOD_TO_GENRE.get(mood.lower(), "chill")
    results = sp.search(q=f"{genre} playlist", type='playlist', limit=1)
    items = results.get('playlists', {}).get('items', [])
    if items:
        return items[0]['external_urls']['spotify']
    return None
