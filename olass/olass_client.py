"""
Goal: Implement the client which sends
json requests to OLASS server.

@authors:
  Andrei Sura <sura.andrei@gmail.com>

@see:
    http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#querying
    http://docs.sqlalchemy.org/en/latest/orm/contextual.html
    https://github.com/requests/requests-oauthlib/blob/master/requests_oauthlib/oauth2_session.py # NOQA
"""
import os
import sys
import json
import requests
from datetime import datetime
from sqlalchemy import text

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
# from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from requests.packages.urllib3.exceptions import InsecureRequestWarning


from olass import utils
from olass import rules
from olass.models import base
from olass.models.patient import Patient
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
        self.engine = utils.get_db_engine(self.config)
        self.session = OlassClient.get_db_session(self.engine, create_tables)
        # self.config.from_object(some_module.DefaultConfig)

    @classmethod
    def get_db_session(cls, engine, create_tables=False):
        """
        Connect to the database and return a Session object

        :param create_tables: boolean used to request table creation
        """
        log.info("Call get_db_session()")
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
        url = self.config.get('TOKEN_URL')
        client_id = self.config.get('CLIENT_ID')
        client_secret = self.config.get('CLIENT_SECRET')
        log.info('TOKEN_URL: {}'.format(url))
        client = BackendApplicationClient(client_id)
        olass = OAuth2Session(client=client)

        try:
            token = olass.fetch_token(
                token_url=url,
                client_id=client_id,
                client_secret=client_secret,
                verify=self.config.get('VERIFY_SSL_CERT', False))
            if token.get('expires_in') == 0:
                if attempt < TOKEN_REQUEST_ATTEMPTS:
                    log.warn("Got an expired token. Re-trying...")
                    return self.get_access_token(self, attempt + 1)
                else:
                    sys.exit("Give up after {} attempts to get a token: {}"
                             .format(TOKEN_REQUEST_ATTEMPTS, url))
        except Exception as exc:
            log.error("get_access_token() problem due: {}".format(exc))
        return token

    @staticmethod
    def get_patient_hashes(session):
        """
        Find patients without `linkage_uuid` and hash their data

        : return patient_map, hashes
        """
        # TODO: the rules for finding patients need to be configurable
        patients = session.query(Patient).filter(
            Patient.pat_birth_date.isnot(None),
            Patient.pat_first_name.isnot(None),
            Patient.pat_last_name.isnot(None),
            Patient.linkage_uuid.is_(None)
        ).limit(200)
        return rules.prepare_patients(patients, rules.RULES_MAP)

    @staticmethod
    def save_response_json(engine, patient_map, json_data):
        """
        http://docs.sqlalchemy.org/en/latest/orm/query.html
        """
        data = json_data.get('data')
        linkage_added_at = datetime.now()

        for i, pat_id in patient_map.items():
            log.info("set linkage_uuid = {} WHERE pat_id = {}"
                     .format(data.get(i).get('uuid'), pat_id))
            linkage_uuid = utils.get_uuid_bin(data.get(i).get('uuid'))
            sql = text('UPDATE patient SET '
                       '    linkage_uuid = :linkage_uuid, '
                       '    linkage_added_at = :linkage_added_at '
                       ' WHERE '
                       '    pat_id = :pat_id')
            engine.execute(sql,
                           linkage_uuid=linkage_uuid,
                           linkage_added_at=linkage_added_at,
                           pat_id=pat_id)
        return True

    @staticmethod
    def send_hashes_to_server(config, engine, token, patient_map, hashes):
        """
        Send the specified dictionary to the OLASS server

        :rtype Boolean
        :return True: if all data was sent to the server and response
                    saved to the local database
        """
        # TODO: should we implement pagination here?
        success = False
        url = config.get('SAVE_URL')
        log.debug("Sending hashes for [{}] patients to [{}]"
                  .format(len(hashes), url))
        client_id = config.get('CLIENT_ID')
        # client_secret = config.get('CLIENT_SECRET')
        client = BackendApplicationClient(client_id)

        try:
            olass = OAuth2Session(client=client, token=token)
            json_data = json.dumps({'data': hashes},
                                   indent=2,
                                   sort_keys=True)
            log.debug(json_data)
            headers = {'Content-Type': 'application/json'}
            response = olass.post(url,
                                  data=json_data.encode('utf-8'),
                                  headers=headers,
                                  verify=config.get('VERIFY_SSL_CERT', False),
                                  )
            response_json = response.json()
            OlassClient.save_response_json(engine, patient_map, response_json)
            success = True
        except Exception as exc:
            log.error("Failed due: {}".format(exc))
        return success

    def run(self):
        """
        Retrieve the unprocessed patients, compute hashes,
        and send data to the OLASS server.
        """
        token = self.get_access_token()
        log.info('Access token: {}'.format(token))
        patient_map, patient_hashes = OlassClient.get_patient_hashes(
            self.session)
        log.info('Got hashes for [{}] patients'.format(len(patient_hashes)))
        done = OlassClient.send_hashes_to_server(self.config,
                                                 self.engine,
                                                 token,
                                                 patient_map,
                                                 patient_hashes)
        if done:
            log.info("All done!")
        else:
            log.info("Fail!")
