"""
Goal: bla
"""
import unittest
# import sqlalchemy as db
from olass.models import base
from olass.olass_client import OlassClient

import logging
lformat = '%(name)s.%(levelname)s ' \
    '- %(filename)s+%(lineno)d: %(message)s'
logging.basicConfig(format=lformat, level=logging.DEBUG)
log = logging.getLogger(__package__)


class BaseTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        log.info('BaseTestCase.__init__')
        super(BaseTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        """ create all tables """
        super(BaseTestCase, self).setUp()
        self.app = OlassClient(config_file='config_tests.py',
                               create_tables=True)
        self.session = self.app.session

    def tearDown(self):
        """ remove all tables """
        # db.session.remove()
        super(BaseTestCase, self).tearDown()
        base.metadata.drop_all(self.app.engine)
