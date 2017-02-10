from __future__ import print_function
from tables.students import Students, get_current_students
from base import loadSession
from sqlalchemy.orm import relationship
from tables.sections import Sections, SectionCourseAff, SectionStudentAff, SectionTeacherAff
from tables.courses import Courses
from tables.sites import Sites
from utils import merge_dicts
import datetime

session = loadSession()

# Get all current students as a dict of student_id's
a = datetime.datetime.now()
current_students = get_current_students(session)
print("Time: {}", (datetime.datetime.now() - a).microseconds)
current_students = {s[0].student_id: s for s in current_students}

"""
All current students organized by site:
    {
        site_id:
            site : <site_table_row_obj>,
            students : [<student_table_row_obj>, ...]
    }
"""

students_by_site = dict()

for id, s in current_students.items():
    site_id = s[2].site_id
    student = s[0]
    if site_id not in students_by_site:
        students_by_site[site_id] = dict({"site": s[2], "students": [student]})
        continue
    site_list = students_by_site[site_id]["students"]
    site_list.append(student)

session.close()
