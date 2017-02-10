from __future__ import print_function
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from utils import foreignkey
from base import Base
from sites import Sites, SiteMixin


class Courses(SiteMixin, Base):
    pass

Sites.courses = relationship("Courses", backref='site')


class CourseMixin(object):

    @declared_attr
    def course_id(self):
        return foreignkey(Courses.course_id)
