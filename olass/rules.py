"""
Goal: Store logic related to hashing data according to
predefined rules.

Authors:
     Andrei Sura <sura.andrei@gmail.com>
"""

# TODO: research the claim from
# L. Sweeney. k-anonymity: a model for protecting privacy.
# International Journal on Uncertainty, Fuzziness and Knowledge-based Systems
#
# "...87% (216 million of 248 million) of the population in the
#   United States had reported characteristics that likely made them
#   unique based only on {5-digit ZIP, gender, date of birth}."

import logging
from olass import utils

log = logging.getLogger(__package__)

# _1 First Name + Last Name + DOB + Zip
RULE_CODE_F_L_D_Z = 'F_L_D_Z'

# _2 Last Name + First Name + DOB + Zip
RULE_CODE_L_F_D_Z = 'L_F_D_Z'

# _3 First Name + Last Name + DOB + City
RULE_CODE_F_L_D_C = 'F_L_D_C'

# _4 Last Name + First Name + DOB + City
RULE_CODE_L_F_D_C = 'L_F_D_C'

# _5 Gender + DOB + Zip
RULE_CODE_G_D_Z = 'G_D_Z'

# In order to guarantee correctness we will allow the partners
# to add to the configuration only values from the map below.
# If we add new rules then we will ask the partners to download a new version
# of the client software.
AVAILABLE_RULES_MAP = {

    RULE_CODE_F_L_D_Z: {
        'required_attr': ['pat_first_name', 'pat_last_name', 'pat_birth_date', 'pat_address_zip'],  # NOQA
        'pattern': '{0.pat_first_name}{0.pat_last_name}{0.pat_birth_date}{0.pat_address_zip}',  # NOQA
    },
    RULE_CODE_L_F_D_Z: {
        'required_attr': ['pat_first_name', 'pat_last_name', 'pat_birth_date', 'pat_address_zip'],  # NOQA
        'pattern': '{0.pat_last_name}{0.pat_first_name}{0.pat_birth_date}{0.pat_address_zip}',  # NOQA
    },
    RULE_CODE_F_L_D_C: {
        'required_attr': ['pat_first_name', 'pat_last_name', 'pat_birth_date', 'pat_address_city'],  # NOQA
        'pattern': '{0.pat_first_name}{0.pat_last_name}{0.pat_birth_date}{0.pat_address_city}',  # NOQA
    },
    RULE_CODE_L_F_D_C: {
        'required_attr': ['pat_first_name', 'pat_last_name', 'pat_birth_date', 'pat_address_city'],  # NOQA
        'pattern': '{0.pat_last_name}{0.pat_first_name}{0.pat_birth_date}{0.pat_address_city}',  # NOQA
    },

    # TODO: review
    RULE_CODE_G_D_Z: {
        'required_attr': ['pat_gender', 'pat_birth_date', 'pat_address_zip'],  # NOQA
        'pattern': '{0.pat_gendere}{0.pat_birth_date}{0.pat_address_zip}',  # NOQA
    },

}


def get_hashes(patient, hashing_rules, salt):
    """
    Get a dictionary of unhexlified hashes for a patient.
    The number of entries in the dictionary depends on the
    "number of rules that can be applied" to a specific patient

    :param hashing_rules: a list of hashing rules codes
    :rtype dict

    .. seealso::

        Called by :meth:`prepare_patients`

    """
    hashes = {}
    count = 0

    for rule in hashing_rules:
        rule_data = AVAILABLE_RULES_MAP.get(rule)
        pattern = rule_data['pattern']
        required_attr = rule_data['required_attr']

        if not patient.has_all_data(required_attr):
            log.debug("Skip hashing patient [{}] due to missing data"
                      "for rule [{}]".format(patient.id, rule))
            continue
        raw = pattern.format(patient) + salt
        chunk = utils.apply_sha256(raw)
        log.debug("Rule {} raw data: {}, hashed: {}".format(rule, raw, chunk))
        hashes[str(count)] = chunk
        count = count + 1

    return hashes


class NormalizedPatient():
    """
    Helper class used to normalize the strings by
    removing punctuation and transforming to lowercase.

    .. seealso::

        Called by :meth:`utils.prepare_for_hashing`
    """
    def __init__(self, pat):
        self.id = pat.id

        self.pat_gender = utils.prepare_for_hashing(
            pat.pat_gender
        )

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

    def has_all_data(self, required_attributes):
        """
        :return bool: `True` if all `required_attributes` have a
        non-empty value
        """
        # TODO: should we check for minimum length of each string?
        for attr in required_attributes:
            if not getattr(self, attr, None):
                log.debug("--> Missing value for attr [{}]".format(attr))
                return False
        return True

    def __repr__(self):
        return "NormalizedPatient " \
            "<pat_gender: {0.pat_gender}, " \
            "pat_birth_date: {0.pat_birth_date}, " \
            "pat_first_name: {0.pat_first_name}, " \
            "pat_last_name: {0.pat_last_name}, " \
            "pat_address_city: {0.pat_address_city}, " \
            "pat_address_zip: {0.pat_address_zip}>".format(self)


def prepare_patients(patients, hashing_rules, salt):
    """
    Calculate hashes for patients.

    :param patients: a list of patients for which we need
                     to retrieve `linkage_uuid` from OLASS server
    :rtype tuple(dict, dict)
    :return two data dictionaries:
        - lut_patient_id structure:
            {0 => pat_id, 1 => pat_id...}
        - lut_patient_hashes structure:
            {0 => {'0' => 'sha_rule_1', '1' => 'sha_rule_2', ...},
            {1 => {'0' => 'sha_rule_1', '1' => 'sha_rule_2', ...},
             ...
            }

    .. seealso::

        Called by :meth:`olass_client.get_patient_data`

    """
    lut_patient_hashes = {}
    lut_patient_id = {}

    for count, patient in enumerate(patients):
        norm_patient = NormalizedPatient(patient)
        pat_hashes = get_hashes(norm_patient, hashing_rules, salt)
        lut_patient_hashes[str(count)] = pat_hashes
        lut_patient_id[str(count)] = patient.id
        log.debug("Hashing: {} \n{}".format(norm_patient, pat_hashes))

    return lut_patient_id, lut_patient_hashes
