#!/usr/bin/env python3
'''Export playlists from Spotify to a file'''
import os
from spotifyclient import SpotifyClient
from utils import save_json, load_json, clean_playlist_data

if __name__ == "__main__":
    # Initialize the Spotify client
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    client = SpotifyClient(client_id, client_secret)
    USER_NAME = 'cakeisreallydeadnow'
    # Fetch the playlists and store to a file
    playlists = client.fetch_playlists(USER_NAME)

    cleaned_playlists = clean_playlist_data(playlists, USER_NAME)

    data = []
    for playlist in cleaned_playlists:
        data.append({
            'name': playlist['name'],
            'owner': playlist['owner'],
            'tracks': client.get_playlist_tracks(playlist['id'])
        })
    save_json(data, 'playlist_data.json')
