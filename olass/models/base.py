"""
Goal: implement the base class for models
"""
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext import declarative

maker = sessionmaker(autoflush=True, autocommit=False)
DBSession = scoped_session(maker)


class ReprBase():

    """
    Provides a nicer representation when a class instance is printed.
    """

    def __repr__(self):
        """
        Note: does not print attributes with "_" as prefix
        """
        return "%s(%s)" % (
            (self.__class__.__name__),
            ', '.join(["%s=%r" % (key, getattr(self, key))
                       for key in sorted(self.__dict__.keys())
                       if not key.startswith('_')]))

DeclarativeBase = declarative.declarative_base(cls=ReprBase)
metadata = DeclarativeBase.metadata


def init(engine):
    """
    Call this method before using any of the ORM classes.

    :seealso: :meth:olass_client.get_db_session()
    """
    DBSession.configure(bind=engine)

# remember to define __ALL__ in each entity we define
from olass.models.patient import *  # NOQA
