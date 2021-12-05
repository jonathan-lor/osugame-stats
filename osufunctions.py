import requests
from os import getenv

API_URL = 'https://osu.ppy.sh/api/v2'
TOKEN_URL = 'https://osu.ppy.sh/oauth/token'


def getToken():
    data = {
        'client_id': getenv('OSU_CLIENT_ID'),
        'client_secret': getenv('OSU_CLIENT_SECRET'),
        'grant_type': 'client_credentials',
        'scope': 'public'
    }

    response = requests.post(TOKEN_URL, data=data)

    return response.json().get('access_token')
