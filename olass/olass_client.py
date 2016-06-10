"""
Goal: Implement the client which sends
json requests to OLASS server.

@authors:
  Andrei Sura <sura.andrei@gmail.com>

https://github.com/requests/requests-oauthlib/blob/master/requests_oauthlib/oauth2_session.py # NOQA
"""
import os
import sys

import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from olass.models import base
# import sqlalchemy as db
import logging

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# TODO: move logging config to a helper function
basedir, f = os.path.split(__file__)
log_conf = os.path.join(basedir, 'logging.conf')

if os.path.exists(log_conf):
    logging.config.fileConfig(log_conf)
else:
    lformat = '%(name)s.%(levelname)s ' \
              '- %(filename)s+%(lineno)d: %(message)s'
    logging.basicConfig(format=lformat, level=logging.INFO)

log = logging.getLogger(__package__)
log.debug("logging was configured...")
alog = logging.getLogger('requests_oauthlib')
alog.addHandler(logging.StreamHandler(sys.stdout))
alog.setLevel(logging.INFO)

TOKEN_REQUEST_ATTEMPTS = 3


class OlassClient():

    def __init__(self, config_file, create_tables=False,
                 root_path='.', default_config={}):
        """
        Setup the database connection obtain an access token
        """
        from olass.config import Config
        self.config = Config(
            root_path=root_path,
            defaults=default_config)
        self.config.from_pyfile(config_file)
        self.db_session = self.get_db_session(create_tables)
        self.acess_token = self.get_access_token()
        # self.config.from_object(some_module.DefaultConfig)

    def get_db_url(self):
        """
        Generate from the config pieces
        """
        # return 'sqlite:///:memory:'
        return 'sqlite:///db.sqlite'

    def get_db_session(self, create_tables=False):
        """
        Connect to the database and return a Session object

        :param create_tables: boolean used to request table creation
        """
        log.info("Call get_db_session()")
        url = self.get_db_url()
        log.debug("get_db_session({})".format(url))
        engine = base.db.create_engine(url, echo=False)
        base.init(engine)
        session = base.DBSession()

        if create_tables:
            base.metadata.create_all(engine)

        return session

    def get_access_token(self, attempt=0):
        """
        Connects to the TOKEN_URL endpoint to retrieve a token.
        """
        log.info('Call get_access_token(attempt={})'.format(attempt))
        log.info('TOKEN_URL: {}'.format(self.config['TOKEN_URL']))
        client = BackendApplicationClient(self.config['CLIENT_ID'])
        olass = OAuth2Session(client=client)

        try:
            token = olass.fetch_token(
                token_url=self.config['TOKEN_URL'],
                client_id=self.config['CLIENT_ID'],
                client_secret=self.config['CLIENT_SECRET'],
                verify=self.config['VERIFY_SSL_CERT'])
        except TokenExpiredError as exc:
            if attempt < TOKEN_REQUEST_ATTEMPTS:
                log.warn("Try to get a fresh token: {}".format(exc))
                return self.get_access_token(self, attempt+1)
            else:
                log.error("Give up after {} attempts to get a token: {}"
                          .format(TOKEN_REQUEST_ATTEMPTS,
                                  self.config['TOKEN_URL']))
        return token

    def get_patient_hashes(self):
        return ({}, 0)

    def run(self):
        """
        Retrieve the unprocessed patients, compute hashes,
        and send data to the OLASS server.
        """
        log.info('Access token: {}'.format(self.acess_token))
        patient_hashes, count = self.get_patient_hashes()
        log.info('Got hashes for [{}] patients'.format(count))

        for id, patient in patient_hashes.items():
            print("{}: {}".format(id, patient))
