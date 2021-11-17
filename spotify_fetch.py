import os
import json
import pandas as pd
import requests


'''
Information on how to set environment variables: https://spotipy.readthedocs.io/en/2.19.0/#redirect-uri
'''


SPOTIPY_REDIRECT_URI = "http://localhost:5555"
SPOTIPY_CLIENT_ID = "1501cd1d65ad49c8bfc8e55c1da10843"
SPOTIPY_CLIENT_SECRET = "59e88c92c64c4ff1b3c1ade1ae1279f0" 


def auth():
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

    return access_token

def test(song_title, access_token, type):

    headers = {
        'Authorization': 'Bearer {token}'.format(token = access_token)
    }

    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'

    # Track ID from the URI
    track_id = 'search?q={song_title}&limit=1&offset=0&type={type}'.format(song_title = song_title, type = type)

    # actual GET request with proper header
    r = requests.get(BASE_URL + track_id, headers=headers, timeout = 10)

    if not r.status_code == 200:
        return None 

    else:
        r = r.json()
        return r


def aud_features(id, access_token):

    headers = {
        'Authorization': 'Bearer {token}'.format(token = access_token)
    }

    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'

    # Track ID from the URI
    track_id = "audio-features/?ids={id}".format(id = id)

    # actual GET request with proper header
    r = requests.get(BASE_URL + track_id, headers=headers)

    if not r.status_code == 200:
        return None
    
    elif r == None:
        return None

    else:
        r = r.json()
        return r

class SpFetch:

    def __init__(self):
        self._token = auth()

    def fetch(self, song_title):

        token = self._token

        results = test(song_title, token, 'track')
        #print("Results: {}".format(results))

        if not results == None: 
            
            if not results['tracks']['items'] == [] and not results == [None] and not results['tracks']['items'][0]['album']['images'] == []:

                #audio_results = sp.audio_features(results['tracks']['items'][0]['id'])
                audio_results = aud_features(results['tracks']['items'][0]['id'], token)['audio_features']
                #print(audio_results)

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


                    #print(json.dumps(data, indent = 4))

                    return data
                
                else:
                    return None      

            else:
                return None

        else:
            return None


if __name__ == "__main__":
    #test()
    
    sp = SpFetch
    sp.fetch("Battery Park")