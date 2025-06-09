import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp_oauth = SpotifyOAuth(
    client_id='7b1d57914c2b40bd8130c2be277cdd96',
    client_secret='b3546f6f758f4e9ba9e42d41a164e756',
    redirect_uri='http://localhost:8888/callback',
    scope='user-read-playback-state user-modify-playback-state user-read-currently-playing',
    cache_path=".cache"
)
sp = spotipy.Spotify(auth_manager=sp_oauth)
def play():
    sp.start_playback()

def pause():
    sp.pause_playback()

def next_track():
    sp.next_track()

def previous_track():
    sp.previous_track()

def play_song(song_name):
    results = sp.search(q=song_name, type='track', limit=1)
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[track_uri])
    else:
        return "❌ Song not found."
