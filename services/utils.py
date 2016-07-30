""" Auth Utils

"""

import cloudstorage as gcs
import endpoints
import json
import os
import webapp2
import logging
import re
from datetime import datetime
from datetime import date
from google.appengine.api import app_identity
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.api import users
from apiclient.discovery import build

from models import ActivityPost
from models import ActivityRecord
from models import Account
from models import activity_record as ar


# NON VALID ACCOUNT TYPES (FOR HARVESTING) : ['deleted', 'administrator']
VALID_ACCOUNT_TYPES = ['active', 'gde', 'marketing', 'productstategy', 'ux_ui']

my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)

gcs.set_default_retry_params(my_default_retry_params)


def get_so_api_key():
    bucket = '/' + os.environ.get('BUCKET_NAME',
                                  app_identity.get_default_gcs_bucket_name())

    secrets_file = None

    try:
        secrets_file = gcs.open(bucket + '/' + 'secrets.json', 'r')
    except gcs.NotFoundError:
        logging.error('secrets.json not found in default bucket')
        return None

    secrets = json.loads(secrets_file.read())
    return secrets.get('so_api_key')


def get_admin_api_key():
    bucket = '/' + os.environ.get('BUCKET_NAME',
                                  app_identity.get_default_gcs_bucket_name())

    secrets_file = None

    try:
        secrets_file = gcs.open(bucket + '/' + 'secrets.json', 'r')
    except gcs.NotFoundError:
        logging.error('secrets.json not found in default bucket')
        return None

    secrets = json.loads(secrets_file.read())
    return secrets.get('admin_api_key')


def get_server_api_key():
    bucket = '/' + os.environ.get('BUCKET_NAME',
                                  app_identity.get_default_gcs_bucket_name())

    secrets_file = None

    try:
        secrets_file = gcs.open(bucket + '/' + 'secrets.json', 'r')
    except gcs.NotFoundError:
        logging.error('secrets.json not found in default bucket')
        return None

    secrets = json.loads(secrets_file.read())
    return secrets.get('server_api_key')


def _getUserId():
    """A workaround implementation for getting userid."""

    auth = os.getenv('HTTP_AUTHORIZATION')
    bearer, token = auth.split()
    token_type = 'id_token'
    if 'OAUTH_USER_ID' in os.environ:
        token_type = 'access_token'
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?%s=%s'
           % (token_type, token))
    user = {}
    wait = 1
    for i in range(3):
        resp = urlfetch.fetch(url)
        if resp.status_code == 200:
            user = json.loads(resp.content)
            break
        elif resp.status_code == 400 and 'invalid_token' in resp.content:
            url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?%s=%s'
                   % ('access_token', token))
        else:
            time.sleep(wait)
            wait = wait + i
    return user.get('user_id', '')


def get_current_account():
    """Retrieve the Account entity associated with the current user."""

    user = endpoints.get_current_user()
    if user is None:
        logging.info('get_current_user returned none')
        return None

    email = user.email().lower()
    logging.info(email)

    # Try latest recorded auth_email first
    accounts = Account.query(Account.auth_email == email).fetch(1)
    if len(accounts) > 0:
        logging.info('auth_email returns')
        return accounts[0]

    # Try the user's default email next
    accounts = Account.query(Account.email == email).fetch(1)
    if len(accounts) > 0:
        # Store auth email for next time
        accounts[0].auth_email = email
        accounts[0].put()
        logging.info('default email returns')
        return accounts[0]

    # Try via the user's Google ID
    user_id = _getUserId()
    accounts = Account.query(Account.gplus_id == user_id).fetch(1)
    if len(accounts) > 0:
        # Store auth email for next time
        accounts[0].auth_email = email
        accounts[0].put()
        logging.info('Google ID returns')
        return accounts[0]

    logging.info('None returns')
    return None


def check_auth(email, api_key):
    if api_key is not None and api_key == get_admin_api_key():
        return True

    accounts = Account.query(Account.email == email).fetch(1)
    if email is not None and endpoints.get_current_user() is not None and len(accounts) == 1:
        return email == endpoints.get_current_user().email() and email == accounts[0].email

    return False
