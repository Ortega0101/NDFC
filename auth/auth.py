import requests
import logging
import sys

from parts import BASE_URL, VERIFY_SSL


def get_token(username, password):
    login_url = f'{BASE_URL}/login'
    credentials = {
        'username': username,
        'password': password
    }

    response = requests.post(login_url, json=credentials, verify=VERIFY_SSL)

    if response.ok:
        token = response.json().get('jwttoken')
        print('Token: Ok')
    else:
        logging.critical(
            'Login failed:', response.text
        )
        sys.exit(1)

    return token
