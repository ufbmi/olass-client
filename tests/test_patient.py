"""
Goal: Test CRUD actions (insert/update/delete)

Authors:
     Andrei Sura <sura.andrei@gmail.com>
"""
import logging
# from mock import patch
# from hashlib import sha256
# from binascii import unhexlify, hexlify
from base_test import BaseTestCase
from olass import utils
from olass.models.patient import Patient

lformat = '%(name)s.%(levelname)s ' \
    '- %(filename)s+%(lineno)d: %(message)s'
logging.basicConfig(format=lformat, level=logging.INFO)
log = logging.getLogger(__name__)


class TestPatient(BaseTestCase):

    """ Add data... """

    def setUp(self):
        super(TestPatient, self).setUp()
        self.create_patients()

    def create_patients(self):
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

        p2 = Patient.get_by_id(1)
        self.assertIsNotNone(p2)
        log.info("Got patient: {}".format(p2))

        p2.update(pat_first_name='updated', pat_last_name='')
        p2 = Patient.get_by_id(1)
        self.assertEquals("updated", p2.pat_first_name)
        self.assertEquals("", p2.pat_last_name)

        p2.delete()
        p2 = Patient.get_by_id(1)
        self.assertIsNone(p2)
