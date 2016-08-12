"""
Goal: Test CRUD actions (insert/update/delete)

Authors:
     Andrei Sura <sura.andrei@gmail.com>
"""
import logging
from datetime import datetime
from base_test import BaseTestCase
from olass import utils
from olass import rules
from olass.rules import NormalizedPatient
from olass.models.patient import Patient

lformat = '%(name)s.%(levelname)s ' \
    '- %(filename)s+%(lineno)d: %(message)s'
logging.basicConfig(format=lformat, level=logging.INFO)
log = logging.getLogger(__name__)


class TestPatient(BaseTestCase):

    """ Add data... """

    def setUp(self):
        super(TestPatient, self).setUp()

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

        p2.update(pat_first_name='updated',
                  pat_last_name='xyz',
                  linkage_added_at=datetime.now(),
                  pat_address_zip='19116')
        p2 = Patient.get_by_id(1)
        self.assertEquals("updated", p2.pat_first_name)
        self.assertEquals("xyz", p2.pat_last_name)
        self.assertIsNotNone(p2.linkage_added_at)

        # Test normalized patients hashing -- since the city is
        # missing only 2 out of 4 hashes will be computed
        patients = self.session.query(Patient).limit(2)
        hashing_rules = ['F_L_D_Z', 'L_F_D_Z', 'F_L_D_C', 'L_F_D_C']
        required_attr = ['pat_last_name', 'pat_first_name',
                         'pat_address_zip', 'pat_birth_date']
        salt = 'himalayan_salt'

        for count, patient in enumerate(patients):
            norm_patient = NormalizedPatient(patient)
            pat_hashes = rules.get_hashes(norm_patient, hashing_rules, salt)
            self.assertIs(len(pat_hashes), 2)
            print('==> {} Check has {} values for {}'
                  .format(count, required_attr, norm_patient))
            self.assertTrue(norm_patient.has_all_data(required_attr))

        patient_map, patient_hashes = rules.prepare_patients(patients,
                                                             hashing_rules,
                                                             salt)
        self.assertIsNotNone(patient_map)
        self.assertIsNotNone(patient_hashes)
        one_patient_hashes = patient_hashes.get('0')
        hash_0 = one_patient_hashes.get('0')
        hash_1 = one_patient_hashes.get('1')
        self.assertEqual(hash_0, 'df8ea7e428b3acf3379436a26e070fed65d0adad80e03cc87c84e82309fc3554')  # NOQA
        self.assertEqual(hash_1, '83293e03c1c00ff49abb0ed5900470942bdf41750e3956135308da40771b692b')  # NOQA

        # Test pagination methods
        # pagination = Patient.query.order_by(
        #     db.desc(Patient.id)).paginate(1, 2)
        # self.assertIs(2, len(pagination.items))

        # for pat in pagination.items:
        #     self.assertIsNotNone(pat)

        # Test deletion
        p2.delete()
        p2 = Patient.get_by_id(1)
        self.assertIsNone(p2)
