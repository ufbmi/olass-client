"""
Goal: Implement the client which sends
json requests to OLASS server.

@authors:
  Andrei Sura <sura.andrei@gmail.com>
"""
import os
from olass.config import Config
from olass.models import base
# import sqlalchemy as db

import logging
basedir, f = os.path.split(__file__)

log_conf = os.path.join(basedir, 'logging.conf')

if os.path.exists(log_conf):
    logging.config.fileConfig(log_conf)
else:
    format = '%(name)s - %(levelname)s ' \
        '- %(filename)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=format, level=logging.NOTSET)

log = logging.getLogger(__package__)
log.debug("logging was configured...")


class OlassClient():

    def __init__(self, config_file, create_tables=False,
                 root_path='.', default_config={}):
        self.config = Config(root_path=root_path, defaults=default_config)
        self.config.from_pyfile(config_file)
        self.session = self.get_db_session(create_tables)
        # self.config.from_object(some_module.DefaultConfig)

    def get_db_url(self):
        """
        Generate from the config pieces
        """
        # return 'sqlite:///:memory:'
        return 'sqlite:///db.sqlite'

    def get_db_session(self, create_tables=False):
        """
        Connect to the database and return a Session object

        :param create_tables: boolean used to request table creation
        """
        url = self.get_db_url()
        log.debug("get_db_session({})".format(url))
        engine = base.db.create_engine(url, echo=False)
        base.init(engine)
        session = base.DBSession()

        if create_tables:
            base.metadata.create_all(engine)

        return session

    def run(self):
        log.info("==> call run()")
        log.debug('Name: {}'.format(self.config['NAME']))
