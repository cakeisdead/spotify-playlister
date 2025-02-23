'''Miscellaneous functions'''
import random
import string


def random_string(length):
    '''Generate a random string with the specified lenght'''
    return ''.join(random.choice(string.ascii_letters) for i in range(length))
