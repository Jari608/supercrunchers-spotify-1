import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
import pandas as pd
import requests

'''
Information on how to set environment variables: https://spotipy.readthedocs.io/en/2.19.0/#redirect-uri
'''

os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:5555"
os.environ["SPOTIPY_CLIENT_ID"] = " " 
os.environ["SPOTIPY_CLIENT_SECRET"] = " " 

SPOTIPY_REDIRECT_URI = "http://localhost:5555"
SPOTIPY_CLIENT_ID = " " 
SPOTIPY_CLIENT_SECRET = " " 

def fetch(song_title):
    
    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope), requests_timeout = 5, retries = 3)

    print("check")

    results = sp.search(song_title, limit = 1, type = 'track')
    print(results)
    if not results['tracks']['items'] == [] and not results == [None] and not results['tracks']['items'][0]['album']['images'] == []:

        audio_results = sp.audio_features(results['tracks']['items'][0]['id'])
        print(audio_results)

        if not audio_results == [None]:
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

    else:
        return None

def test():
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': SPOTIPY_CLIENT_ID,
        'client_secret': SPOTIPY_CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'

    # Track ID from the URI
    track_id = 'search?q=Battery+Park&limit=1&offset=0&type=track'

    # actual GET request with proper header
    r = requests.get(BASE_URL + track_id, headers=headers)

    r = r.json()
    print(r)

if __name__ == "__main__":
    test()
    
    
    fetch("Battery Park")