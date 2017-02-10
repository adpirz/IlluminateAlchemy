from __future__ import print_function
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from utils import foreignkey

from base import Base


class Sites(Base):
    rooms = relationship("Rooms", backref='site')


class SiteMixin(object):

    @declared_attr
    def site_id(self):
        return foreignkey(Sites.site_id)


class Rooms(SiteMixin, Base):
    pass


class RoomMixin(object):

    @declared_attr
    def room_id(self):
        return foreignkey(Rooms.room_id)