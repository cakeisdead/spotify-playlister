#!/usr/bin/env python3
'''Export playlists from Spotify to a file'''
import requests
from threading import Thread
from spotifyclient import *
import json
import os


# def get_playlist_tracks(playlist_id):
#     '''Fetch the tracks of a playlist'''
#     endpoint = f'/playlists/{playlist_id}/tracks'

#     try:
#         if TOKEN == '':
#             get_token()

#         headers = {
#             'Authorization': f'Bearer {TOKEN}'
#         }
#         r = requests.get(BASE_URL + endpoint, headers=headers, timeout=20)
#         r.raise_for_status()
#         tracks = r.json()

#         if 'items' in tracks:
#             for track in tracks['items']:
#                 track_info = track['track']
#                 print(f"Track: {track_info['name']}")
#                 print(
#                     f"Artist: {', '.join(artist['name'] for artist in track_info['artists'])}")
#                 print(f"Album: {track_info['album']['name']}")
#                 print()

#     except requests.exceptions.HTTPError as err:
#         print(f"Error: {err}")


# def parse_playlists():
#     '''Parse the playlists'''
#     with open('playlists.json', 'r', encoding='utf-8') as f:
#         playlists = json.load(f)

#     my_playlists = [f for f in playlists['items']
#                     if f['owner']['id'] == 'cakeisreallydeadnow']

#     for playlist in my_playlists:
#         print(f"Playlist: {playlist['name']}")
#         print(f"ID: {playlist['id']}")
#         print(f"Tracks: {playlist['tracks']['total']}")
#         print(f"Owner: {playlist['owner']['display_name']}")
#         get_playlist_tracks(playlist['id'])
#         print()


if __name__ == "__main__":
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    client = SpotifyClient(client_id, client_secret)
    playlists = client.fetch_playlists('cakeisreallydeadnow')
    print(playlists)

    # with open('playlists.json', 'w', encoding='utf-8') as f:
    #             json.dump(playlists, f, indent=2)
    #         print("Playlists saved to playlists.json")
    # parse_playlists()
