from __future__ import print_function
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Date

from base import Base, base_table_args
from students import Students
from utils import merge_dicts, foreignkey


class AttendanceFlags(Base):
    student_attendance = relationship("DailyRecords", backref="flag")

    """
    Attendance flag info:
      id |code |    flag_text
      ---+-----+--------------------
       1 | X   | Not Enrolled
       2 | N   | School Closed
       3 | D   | Delete
       4 | +   | Present
       5 | T   | Tardy
       6 | A   | Absent
       7 | E   | Excused
       8 | U   | Unexcused
       9 | R   |  Early Release
      10 | L   | Excused Tardy
      11 | M   | Unexcused Tardy
      12 | Y   | T30

     """


class DailyRecords(Base):
    __table_args__ = merge_dicts(base_table_args, {'schema': 'attendance'})
    student_id = foreignkey(Students.student_id, primary_key=True)
    attendance_flag_id = foreignkey(AttendanceFlags.attendance_flag_id, primary_key=True)
    date = Column(Date, primary_key=True)


def get_student_attendance_daily(session, StudentOrID, startdate, enddate=None, flags=None, **kwargs):
    """
    Returns all attendance records from table DailyRecords for individual student
    """
    sid = StudentOrID.student_id if isinstance(StudentOrID, Students) else StudentOrID

    result = session.query(DailyRecords).join(Students).join(AttendanceFlags)\
        .filter(Students.student_id == sid)

    if flags:
        if not isinstance(flags, list):
            flags = [flags]
        result = result.filter(AttendanceFlags.character_code.in_(flags))

    if kwargs:
        for k, v in list(kwargs.items()):
            result = result.filter(getattr(AttendanceFlags, k) == v)

    if enddate:
        return result.filter(DailyRecords.date >= startdate)\
            .filter(DailyRecords.date <= enddate)\
            .distinct(DailyRecords.date)\
            .all()

    return result.filter(DailyRecords.date == startdate)\
        .distinct(DailyRecords.date)\
        .all()
