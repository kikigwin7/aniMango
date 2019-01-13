import codecs
import os.path
import pickle
import requests
import time
import json

from django.core.exceptions import ValidationError

from .anilist_config import aniclient, anisecret, pickle_path

params = {'grant_type': 'client_credentials', 'client_id': aniclient, 'client_secret': anisecret}


def populate_series_item(series_obj):
    try:
        info = api_get_info(series_obj)
    except Exception as e:
        raise ValidationError(repr(e))

    series_obj.title = info['title']['romaji']
    series_obj.title_eng = info['title']['english'] if (info['title']['english'] is not None) else ''
    series_obj.api_id = int(info['id'])
    series_obj.series_type = info['type']

    series_obj.synopsis = info['description']
    series_obj.cover_link = info['coverImage']['large']
    series_obj.ani_link = 'https://anilist.co/{0!s}/{1!s}'.format(str(series_obj.series_type), str(series_obj.api_id))


def api_get_info(series_obj):
    query = '''
    query ($id: Int) { # Define which variables will be used in the query (id)
      Media (id: $id) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
        id
        title {
            romaji
            english
        }
        type
        description
        coverImage {
            large
        }
      }
    }
    '''
    variables = {'id': series_obj.api_id}

    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})

    return json.loads(response.content.decode("utf-8"))['data']['Media']


# This is deprecated but left in in-case anilist api v1 is required
# For future work please look at Anilist API v2 https://github.com/AniList/ApiV2-GraphQL-Docs
def api_get_info_old(series_obj):
    url = 'https://anilist.co/api/{0!s}/{1!s}'.format(str(series_obj.series_type), str(series_obj.api_id))
    try:
        request = requests.get(url, params={'access_token': get_access_token()})

        if request.status_code == 401:
            renew_token()
            request = requests.get(url, params={'access_token': get_access_token()})

        if request.status_code == 200:
            return request.json()
        else:
            raise RuntimeError(
                'Could not retrieve info from AniList. Status code received is ' + str(request.status_code))
    except Exception as e:
        raise


def get_series_by_name(series_type, title):
    query = '''
        query ($name: String) {
  Media(search: $name) {
    id
    title {
      romaji
      english
    }
    type
    description
    coverImage {
      large
    }
  }
}

        '''
    variables = {'name': title}

    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})
    print(response.content)
    return json.loads(response.content)['data']['Media']



# Gets the series json minimised from anilist
def get_series_by_name_old(series_type, title):
    url = 'https://anilist.co/api/{0!s}/search/{1!s}'.format(series_type, title)
    try:
        request = requests.get(url, params={'access_token': get_access_token()})

        if request.status_code == 401:
            renew_token()
            request = requests.get(url, params={'access_token': get_access_token()})

        if request.status_code == 200:
            return request.json()
        else:
            raise RuntimeError(
                'Could not retrieve info from AniList. Status code received is ' + str(request.status_code))
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
