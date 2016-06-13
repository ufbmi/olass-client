#!/usr/bin/env python
"""
Goal: Helper tool for loading sample voter data.

@authors:
  Andrei Sura <sura.andrei@gmail.com>
"""
import logging
from olass import utils
from olass.config import Config

lformat = '%(name)s.%(levelname)s ' \
    '- %(filename)s+%(lineno)d: %(message)s'
logging.basicConfig(format=lformat, level=logging.INFO)
log = logging.getLogger(__package__)

if __name__ == "__main__":
    """ Read args """
    config = Config(root_path='.')
    # defaults=default_config)
    config.from_pyfile('config.py')
    print(config)

    file_in = 'data/fl_ex_samples.csv'
    file_out = 'data/fl_out.csv'
    columns = {
        'pat_mrn': 'v_voter_id',
        # 'gender': 'v_gender',
        # 'race': 'v_race',
        'pat_birth_date': 'v_birth_date',
        'pat_first_name': 'v_name_first',
        'pat_last_name': 'v_name_last',
        'pat_middle_name': 'v_name_middle',
        'pat_address_line1': 'v_residence_address_1',
        'pat_address_line2': 'v_residence_address_2',
        # 'v_residence_address_2
        'pat_address_city': 'v_residence_address_city',
        'pat_address_state': 'v_residence_address_state',
        'pat_address_zip': 'v_residence_address_zip',
        # 'v_daytime_area_code,v_daytime_phone_number
    }
    utils.import_voter_data(file_in, columns, file_out, config)
