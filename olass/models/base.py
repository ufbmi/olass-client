"""
Goal: implement the base class for models
"""
# import sqlalchemy as sa
# from sqlalchemy import orm
from sqlalchemy.orm import sessionmaker, scoped_session
# from sqlalchemy.orm.exc import UnmappedClassError
from sqlalchemy.ext import declarative

maker = sessionmaker(autoflush=True, autocommit=False)
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


# class _QueryProperty(object):
#     def __init__(self, sa):
#         self.sa = sa
#
#     def __get__(self, obj, type):
#         try:
#             mapper = orm.class_mapper(type)
#             if mapper:
#                 # return type.query_class(mapper, session=self.sa.session())
#                 # return orm.Query(mapper, session=self.sa.session())
#                 return orm.Query(mapper...
#         except UnmappedClassError:
#             return None


# def make_declarative_base(model, metadata=None):
#     base = declarative.declarative_base(cls=model, name='Model')
#     # base.query = _QueryProperty(self)
#     # base.query = _QueryProperty(orm.Query)
#     return base


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


DeclarativeBase = declarative.declarative_base(cls=ReprBase)
# DeclarativeBase = make_declarative_base(model=ReprBase)
metadata = DeclarativeBase.metadata

# remember to define __ALL__ in each entity we define
from olass.models.patient import *  # NOQA
