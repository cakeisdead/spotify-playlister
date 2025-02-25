'''Miscellaneous functions'''
import random
import string
import json


def clean_playlist_data(playlists, owner_name):
    '''Filter playlist data by owner name'''
    cleaned_playlists = [
        {
            'name': playlist['name'],
            'id': playlist['id'],
            'owner': playlist['owner']['display_name']
        }
        for playlist in playlists['items']
        if playlist['owner']['display_name'] == owner_name
    ]
    return cleaned_playlists


def load_json(filename):
    '''Load data from a JSON file'''
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"Data loaded from {filename}")
        return data


def save_json(data, filename):
    '''Save data to a JSON file'''
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        print(f"Data saved to {filename}")


def random_string(length):
    '''Generate a random string with the specified lenght'''
    return ''.join(random.choice(string.ascii_letters) for i in range(length))
