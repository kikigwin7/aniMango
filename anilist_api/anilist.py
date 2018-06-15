import os.path
import pickle
import requests
import time

from django.core.exceptions import ValidationError

from .anilist_config import aniclient, anisecret, pickle_path

params = {'grant_type': 'client_credentials', 'client_id': aniclient, 'client_secret': anisecret}

def populate_series_item(series_obj):
    try:
        info = api_get_info(series_obj)
    except Exception as e:
        raise ValidationError(repr(e))
    
    series_obj.title = info['title_romaji']
    series_obj.title_eng = info['title_english']
    series_obj.api_id = int(info['id'])
    series_obj.series_type = info['series_type']
    series_obj.synopsis = info['description']
    series_obj.cover_link = info['image_url_lge']
    series_obj.ani_link = 'https://anilist.co/{0!s}/{1!s}'.format(series_obj.series_type, series_obj.api_id)

def api_get_info(series_obj):
    url = 'https://anilist.co/api/{0!s}/{1!s}'.format(series_obj.series_type, series_obj.api_id)
    try:
        request = requests.get(url, params={'access_token': get_access_token()})

        if request.status_code == 401:
            renew_token()
            request = requests.get(url, params={'access_token': get_access_token()})

        if request.status_code == 200:
            return request.json()
        else:
            raise RuntimeError('Could not retrieve info from AniList. Status code received is '+request.status_code)
    except Exception as e:
        raise

#
# Methods for token management - Sorc
#
def get_access_token():
    if not os.path.isfile(pickle_path):
        renew_token()
    token = get_token_from_pickle()
    if time.time() > token['expires']:
        renew_token()
        token = get_token_from_pickle()
    return token['token']
    
def renew_token():
    try:
        r = requests.post('https://anilist.co/api/auth/access_token', params=params).json()
    except Exception as e:
        raise RuntimeError('Could not renew AniList token.' + repr(e))
    try:
        with open(pickle_path, 'wb') as f:
            pickle.dump({
                'token': r['access_token'],
                'expires': time.time() + int(r['expires_in'])
            }, f)
    except Exception as e:
        raise RuntimeError('Could not dump token to pickle.' + repr(e))

def get_token_from_pickle():
    with open(pickle_path, 'rb') as f:
        return pickle.load(f)