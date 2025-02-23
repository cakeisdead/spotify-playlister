'''Miscellaneous functions'''
import random
import string
import json


def save_json(data, filename):
    '''Save data to a JSON file'''
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        print(f"Data saved to {filename}")


def random_string(length):
    '''Generate a random string with the specified lenght'''
    return ''.join(random.choice(string.ascii_letters) for i in range(length))
