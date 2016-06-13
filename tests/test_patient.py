"""
Goal: Extend the base test class by inserting sample rows in the database

Authors:
     Andrei Sura <sura.andrei@gmail.com>
"""
# from mock import patch
# from hashlib import sha256
# from binascii import unhexlify
# from binascii import hexlify
# from olass import utils
# from datetime import datetime
from base_test import BaseTestCase
from olass import utils
from olass.models.patient import Patient

class TestPatient(BaseTestCase):

    """ Add data... """

    def setUp(self):
        super(TestPatient, self).setUp()
        self.create_patients()

    def create_patients(self):
        # when = datetime.now()
        # when.replace(microsecond=0)
        when = utils.format_date('01-01-1950')
        p1 = Patient.create(
            pat_mrn=1,
            pat_birth_date=when,
            pat_first_name='First',
            pat_last_name='Last'
        )
        self.assertIsNotNone(p1.id)

    def test_read_patients(self):
        """
        Verify that we can properly write to the database.
        """
        when = utils.format_date('01-01-1950')
        p = self.session.query(Patient).filter_by(id='1').one_or_none()
        self.assertIsNotNone(p)
        self.assertEquals(when, p.pat_birth_date)
        self.assertEquals("First", p.pat_first_name)
        self.assertEquals("Last", p.pat_last_name)

        # p2 = Patient.query.get_by_id(1)
        # self.assertIsNotNone(p)
        # print("Got: {}".format(p2))
