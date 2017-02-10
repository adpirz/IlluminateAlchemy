from __future__ import print_function

from base import Base
from sqlalchemy.ext.declarative import declared_attr
from utils import foreignkey


class Users(Base):
    pass


class UserMixin(object):

    @declared_attr
    def user_id(self):
        return foreignkey(Users.user_id)

