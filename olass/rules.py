"""
Goal: Store logic related to hashing data according to
predefined rules.

Authors:
     Andrei Sura <sura.andrei@gmail.com>
"""
import logging
from olass import utils

log = logging.getLogger(__package__)

# _1 First Name + Last Name + DOB + Zip
RULE_CODE_F_L_D_Z = 'F_L_D_Z'  # NOQA

# _2 Last Name + First Name + DOB + Zip
RULE_CODE_L_F_D_Z = 'L_F_D_Z'  # NOQA

# _3 First Name + Last Name + DOB + City
RULE_CODE_F_L_D_C = 'F_L_D_C'  # NOQA

# _4 Last Name + First Name + DOB + City
RULE_CODE_L_F_D_C = 'L_F_D_C'  # NOQA

# _5 Three Letter FN + Three Letter LN + Soundex FN + Soundex LN + DOB
# RULE_CODE_3F_3L_SF_SL_D = '3F_3L_SF_SL_D'  # NOQA


RULES_MAP = {
    RULE_CODE_F_L_D_Z:
        '{0.pat_first_name}{0.pat_last_name}{0.pat_birth_date}{0.pat_address_zip}',  # NOQA
    RULE_CODE_L_F_D_Z:
        '{0.pat_last_name}{0.pat_first_name}{0.pat_birth_date}{0.pat_address_zip}',  # NOQA
    RULE_CODE_F_L_D_C:
        '{0.pat_first_name}{0.pat_last_name}{0.pat_birth_date}{0.pat_address_city}',  # NOQA
    RULE_CODE_L_F_D_C:
        '{0.pat_last_name}{0.pat_first_name}{0.pat_birth_date}{0.pat_address_city}',  # NOQA
}


def get_hashes(patient, rules_map):
    """
    Get a dictionary of unhexlified hashes for a patient
    """
    hashes = {}

    count = 0

    for rule, pattern in rules_map.items():
        raw = pattern.format(patient)
        chunk = utils.apply_sha256(raw)
        log.debug("Rule {} raw data: {}, hashed: {}".format(rule, raw, chunk))
        hashes[str(count)] = chunk
        count = count + 1

    return hashes


class NormalizedPatient():
    """
    Helper class used to ormalize the strings by
    removing punctuation and transforming to lowercase.

    .. seealso::

        :meth:`utils.prepare_for_hashing`
    """
    def __init__(self, pat):
        self.pat_birth_date = utils.format_date_as_string(
            pat.pat_birth_date, utils.FORMAT_DATABASE_DATE
        )
        self.pat_first_name = utils.prepare_for_hashing(
            pat.pat_first_name
        )
        self.pat_last_name = utils.prepare_for_hashing(
            pat.pat_last_name
        )
        self.pat_address_city = utils.prepare_for_hashing(
            pat.pat_address_city
        )
        self.pat_address_zip = utils.prepare_for_hashing(
            pat.pat_address_zip
        )

    def __repr__(self):
        return "NormalizedPatient <pat_birth_date: {0.pat_birth_date}, " \
            "pat_first_name: {0.pat_first_name}, " \
            "pat_last_name: {0.pat_last_name}, " \
            "pat_address_city: {0.pat_address_city}, " \
            "pat_address_zip: {0.pat_address_zip}>".format(self)


def prepare_patients(patients, rules_map):
    """
    Calculate hashes for patients.

    :param patients: a list of patients for which we need
                     to retrieve `linkage_uuid` from OLASS server
    :return ?:
    """
    hashes = {}

    for count, patient in enumerate(patients):
        norm_patient = NormalizedPatient(patient)
        pat_hashes = get_hashes(norm_patient, rules_map)
        hashes[str(count)] = pat_hashes
        log.info("Hashing: {} \n{}".format(norm_patient, pat_hashes))
        # log.debug("MRN: {} hashes: \n{}".format(patient.pat_mrn, pat_hashes))

    return hashes
