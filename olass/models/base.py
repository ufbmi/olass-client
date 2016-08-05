"""
Goal: implement the base class for models
"""
# import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import sessionmaker, scoped_session
# from sqlalchemy.orm.exc import UnmappedClassError
from sqlalchemy.ext import declarative

# http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
maker = sessionmaker(autoflush=True,
                     autocommit=False,
                     expire_on_commit=True)
DBSession = scoped_session(maker)
session = None


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


def init(engine):
    """
    Call this method before using any of the ORM classes.

    :seealso: :meth:olass_client.get_db_session()
    """
    DBSession.configure(bind=engine)


def get_session():
    global session
    if session is None:
        session = DBSession()
    return session


class _QueryProperty():
    """
    """
    # TODO: this class needs access to the session object...
    def __init__(self, sa):
        self.sa = sa

    def __get__(self, obj, type):
        try:
            mapper = orm.class_mapper(type)
            if mapper:
                return type.query_class(mapper, session=self.sa.session())
        except UnmappedClassError:
            return None


DeclarativeBase = declarative.declarative_base(cls=ReprBase)
metadata = DeclarativeBase.metadata


class Model():
    # TODO: document
    query_class = None
    query = None


class NiceSQLAlchemy():
    """
    Provides convenient access to the declarative_base class.
    """

    def __init__(self, model_class=Model, metadata=None):
        # self.session = None  # TODO
        # self.Query = BaseQuery  # TODO
        self.Model = self.make_declarative_base(model_class, metadata)

    def make_declarative_base(self, model_class, metadata=None):
        """Creates the declarative base."""
        base = declarative.declarative_base(cls=model_class,
                                            name='Model',
                                            metadata=metadata,
                                            # metaclass=_BoundDeclarativeMeta
                                            )

        # TODO: why do we need this check here???
        # if not getattr(base, 'query_class', None):
        #     base.query_class = self.Query

        base.query = _QueryProperty(self)
        return base


# remember to define __ALL__ in each entity we define
from olass.models.patient import *  # NOQA
