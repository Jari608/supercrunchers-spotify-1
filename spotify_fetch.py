import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
import pandas as pd

'''
Information on how to set environment variables: https://spotipy.readthedocs.io/en/2.19.0/#redirect-uri
'''

os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:5555"
os.environ["SPOTIPY_CLIENT_ID"] = "8488471ad2d143a59c1640bed0057987" 
os.environ["SPOTIPY_CLIENT_SECRET"] = "00fd4982e9ba4d1ea156a8fd00039a47" 

def fetch(song_title):
    
    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = sp.search(song_title, limit = 1, type = 'track')

    if not results['tracks']['items'] == []:
        audio_results = sp.audio_features(results['tracks']['items'][0]['id'])

        data = {}
        data['track_id'] = results['tracks']['items'][0]['id']
        data['track_name'] = results['tracks']['items'][0]['name']
        data['popularity'] = results['tracks']['items'][0]['popularity']
        data['preview_url'] = results['tracks']['items'][0]['preview_url']
        data['track_number'] = results['tracks']['items'][0]['track_number']
        data['first_artist'] = results['tracks']['items'][0]['album']['artists'][0]['name']
        data['image_url'] = results['tracks']['items'][0]['album']['images'][0]['url']
        data['spotify_url'] = results['tracks']['items'][0]['external_urls']['spotify']
        data['acousticness'] = audio_results[0]['acousticness']
        data['danceability'] = audio_results[0]['danceability']
        data['duration_ms'] = audio_results[0]['duration_ms']
        data['energy'] = audio_results[0]['energy']
        data['instrumentalness'] = audio_results[0]['instrumentalness']
        data['key'] = audio_results[0]['key']
        data['liveness'] = audio_results[0]['liveness']
        data['loudness'] = audio_results[0]['loudness']
        data['speechiness'] = audio_results[0]['speechiness']
        data['tempo'] = audio_results[0]['tempo']
        data['time_signature'] = audio_results[0]['time_signature']
        data['valence'] = audio_results[0]['valence']

        print(json.dumps(data, indent = 4))

        return data
    
    else:
        return None

if __name__ == "__main__":
    fetch('donna summer i feel love')