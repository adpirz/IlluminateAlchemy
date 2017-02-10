from __future__ import print_function
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker
from utils import camel_to_underscore

"""
Creates base SQL Alchemy declarative class with
PostgreSQL engine.
"""

USERNAME = '<USERNAME>'
PASSWORD = '<PASSWORD>'
DOMAIN = 'db.illuminateed.com'
PORT = '5436'
DATABASE = USERNAME

ENGINE_STRING = "postgres://{U}:{PW}@{D}:{PO}/{DB}".format(
    U=USERNAME, PW=PASSWORD, D=DOMAIN, PO=PORT, DB=DATABASE
)
engine = create_engine(ENGINE_STRING)

base_table_args = {'autoload': True}


class Base(object):

    @declared_attr
    def __tablename__(self):
        # Easily convert Python class conventions to table names
        return camel_to_underscore(self.__name__)

    __table_args__ = base_table_args

Base = declarative_base(engine, cls=Base)


def loadSession():
    return sessionmaker(bind=engine)()
