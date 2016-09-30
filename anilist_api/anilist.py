import requests
import sys
import traceback
import time
import json
from .anilist_config import aniclient, anisecret

# The anilist api uses numbers > 30000 for manga pages and below for anime
# I dont know why, it just is
ANILIST_MAGIC_NUMBER = 30000

ANICLIENT = aniclient
ANISECRET = anisecret

access_token = ''

def check_and_get_old_token():
    try:
        # open the file if it exists
        #print('Checking for old token')
        token_file = open('anilist.token', 'r+')
        token_json = json.load(token_file)
        time_now = time.time()

        if time_now < token_json['expires']:
            global access_token
            access_token = token_json['access_token']
            token_file.close()
            #print('Old token checked and valid')
            return True
        else:
            token_file.close()
            #print('Old token checked and invalid')
            return False

    except Exception as e:
        # Token file doesnt exist or there was some other error
        # create a new empty token file
        #print('No existing token found')
        open('anilist.token', 'w').close()
        return False

def get_new_token():
    try:
        #print ('Trying to get new anilist token')
        request = requests.post(
            'https://anilist.co/api/auth/access_token',
            params={
                'grant_type':'client_credentials',
                'client_id':ANICLIENT,
                'client_secret':ANISECRET
            }
        )
        #print ('Gained anilist token')

        #print('Writing anilist token')
        request_json = request.json()
        f = open('anilist.token', 'w')
        json.dump(request_json, f)
        f.close()

        global access_token
        access_token = request_json['access_token']

    except Exception as e:
        traceback.print_exc()
        #print('Error getting anilist api token')

def setup():
    if check_and_get_old_token():
        return
    else:
        #print('No valid existing token')
        get_new_token()

def api_get_info(media_id):
    url = 'https://anilist.co/api/'
    # 30000 is the anilist cutoff value for manga 
    # MAGIC NUMBERS
    if media_id > ANILIST_MAGIC_NUMBER:
        url += 'manga/'
    else:
        url += 'anime/'

    url += str(media_id) + '/page'

    try:
        request = requests.get(url, params={'access_token':access_token})

        if request.status_code == 401:
            setup()
            request = requests.get(url, params={'access_token':access_token})

        if request.status_code == 200:
            return request.json()
        else:
            return None
    except Exception as e:
        traceback.print_exc()
        return None
