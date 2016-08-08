"""
Goal: create a session and database tables
so we can run data tests

@see https://docs.python.org/3/library/unittest.mock-examples.html
"""
import unittest
# from binascii import unhexlify
from mock import patch
from olass import utils
from olass.models import base
from olass.olass_client import OlassClient
from olass.models.patient import Patient


def dummy_get_access_token(*args, **kwargs):
    return None


def dummy_get_patient_hashes(*args, **kwargs):
    return {}, {}


def dummy_send_hashes_to_server(*args, **kwargs):
    return True


class BaseTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)

    @patch.multiple(OlassClient,
                    get_access_token=dummy_get_access_token,
                    # get_patient_hashes=dummy_get_patient_hashes,
                    send_hashes_to_server=dummy_send_hashes_to_server)
    def setUp(self):
        """ create all tables """
        super(BaseTestCase, self).setUp()
        self.app = OlassClient(config_file='config/settings_tests.py',
                               interactive=False,
                               create_tables=True)
        self.session = self.app.session
        self.create_patients()
        # TODO: move this line to a dedicated test
        self.app.run()

    def tearDown(self):
        """ remove all tables """
        super(BaseTestCase, self).tearDown()
        base.metadata.drop_all(self.app.engine)
        # self.app.session.remove()

    def create_patients(self):
        when = utils.format_date('01-01-1950')
        Patient.create(
            pat_mrn=1,
            pat_birth_date=when,
            pat_first_name='First',
            pat_last_name='Last'
        )
