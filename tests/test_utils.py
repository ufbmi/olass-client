"""
Goal: test utils.py

Authors:
    Andrei Sura <sura.andrei@gmail.com>
"""
import unittest
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

    def test_list_grouper(self):
        """
        Verify the grouping functionality
        """
        data = list('abcdefg')
        groups = utils.list_grouper(data, 3)
        count = 0

        for group in groups:
            count = count + 1

            if count == 1:
                self.assertEqual(list(group), ['a', 'b', 'c'])
            elif count == 2:
                self.assertEqual(list(group), ['d', 'e', 'f'])
            else:
                self.assertEquals(list(group), ['g', None, None])
        self.assertIs(count, 3)

    def test_dict_grouper(self):
        """
        Verify the grouping functionality
        """
        from collections import OrderedDict
        data = OrderedDict(
            {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 'g': 7})
        chains = utils.dict_grouper(data, 3)

        count = 0

        for chain in chains:
            count = count + 1

            if count == 1:
                self.assertEqual(dict(chain), {1: 'a', 2: 'b', 3: 'c'})
            elif count == 2:
                self.assertEqual(dict(chain), {4: 'd', 5: 'e', 6: 'f'})
            else:
                self.assertEqual(dict(chain), {'g': 7})

        self.assertIs(count, 3)

if __name__ == '__main__':
    unittest.main()
