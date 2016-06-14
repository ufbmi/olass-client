
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

    def test_prepare_for_hashing(self):
        """Verify that punctuation characters are removed """
        subjects = {
            '1': {'in': 'AbC xyZ', 'out': 'abcxyz'},
            '2': {'in': 'A&B,C.D:E;F-G}{H!?I@#', 'out': 'abcdefghi'},
            '3': {'in': 'A^B|C', 'out': 'a^b|c'},
        }

        for case, data in subjects.items():
            self.assertEqual(data.get('out'),
                             utils.prepare_for_hashing(data.get('in')))
