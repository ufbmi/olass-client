
from base_test import BaseTestCase
from olass import utils
from olass.config import Config
config = Config(root_path='tests/')


class TestUtils(BaseTestCase):

    def test_import_voter_data(self):
        file_in = 'tests/voter_in.csv'
        file_out = 'tests/voter_out.csv'
        columns = {
            'pat_mrn': 'mrn',
            'pat_birth_date': 'birth_date',
            'pat_first_name': 'first_name',
            'pat_last_name': 'last_name',
        }
        utils.import_voter_data(file_in, columns, file_out, self.app.config)
