from __future__ import print_function
from sqlalchemy import text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from utils import merge_dicts, foreignkey

from base import Base, base_table_args
from sites import Sites


class Students(Base):
    rosters = relationship("CurrentStudentRoster", backref="student")


class StudentMixin(object):

    @declared_attr
    def student_id(self):
        return foreignkey(Students.student_id)


class CurrentStudentRoster(Base):
    __tablename__ = 'ss_current'
    __table_args__ = merge_dicts(base_table_args, {"schema": "matviews"})
    site_id = foreignkey(Sites.site_id, primary_key=True)
    student_id = foreignkey(Students.student_id, primary_key=True)
    roster_site = relationship("Sites")
    roster_student = relationship("Students")


def get_current_students(session, text_query=None, return_roster_tuple=True, return_query=False):
    """
    Return all currently rostered students from ss_current table.

    :param session: SQLAlchemy session
    :param text_query: SQL statement or SQL Alchemy expression to filter
        ex: 'sites.site_id = 123', 'SELECT * FROM students, sites WHERE sites.site_id=123'
    :param return_roster_tuple: Returns tuple of student, roster, and
        site if true; only students when false
    :param return_query: when True, returns a SQL Alchemy chainable
        query instead of list of results
    """

    if return_roster_tuple:
        q = session.query(Students, CurrentStudentRoster, Sites)
    else:
        q = session.query(Students).join(CurrentStudentRoster).join(Sites)

    results = q.filter(Students.student_id == CurrentStudentRoster.student_id) \
        .filter(CurrentStudentRoster.site_id == Sites.site_id) \
        .distinct(CurrentStudentRoster.student_id)

    if not text_query:
        if return_query:
            return results

        return results.all()

    results = results.filter(text(text_query))

    if return_query:
        return results

    return results.all()
