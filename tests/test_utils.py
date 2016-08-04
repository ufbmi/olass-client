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

    def test_prepare_for_hashing(self):
        """Verify that punctuation characters are removed """
        subjects = {
            '1': {'in': 'AbC xyZă', 'out': 'abcxyză'},
            '2': {'in': 'A&B,C.D:E;F-G}H{I@#J!', 'out': 'abcdefghij'},
            '3': {'in': 'ABC!"#$%&\'()*+,-./:;=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c', 'out': 'abc'},  # NOQA
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

    @unittest.skip("this is not working consistently")
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
