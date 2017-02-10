from __future__ import print_function
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from utils import foreignkey

from base import Base
from sites import Rooms, RoomMixin
from users import Users, UserMixin
from students import Students, StudentMixin
from courses import CourseMixin


class Sections(RoomMixin, Base):
    # teachers = relationship("Users", secondary="SectionTeacherAff", backref='section')
    # students = relationship("Students", secondary="SectionStudentAff", backref='section')
    pass

Rooms.sections = relationship("Sections", backref="room")


class SectionMixin(object):

    @declared_attr
    def section_id(self):
        return foreignkey(Sections.section_id)


class SectionTeacherAff(SectionMixin, UserMixin, Base):
    pass


class SectionCourseAff(SectionMixin, CourseMixin, Base):
    pass


class SectionStudentAff(SectionMixin, StudentMixin, CourseMixin, Base):
    pass


if __name__ == "__main__":
    from base import loadSession
    from students import get_current_students
    s = loadSession()
    x = get_current_students(s, return_query=True)
    s.query(Sections)