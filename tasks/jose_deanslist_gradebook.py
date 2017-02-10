from tables.gradebooks import OverallScoreCache
from tables.students import Students, CurrentStudentRoster
from base import loadSession
from sqlalchemy import and_

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import Encoders

import csv
import smtplib
import json

s = loadSession()
csr = CurrentStudentRoster
st = Students
osc = OverallScoreCache
r = s.query(st, osc)\
    .join(csr)\
    .filter(and_(csr.student_id == st.student_id, csr.site_id == 2))\
    .filter(st.student_id == osc.student_id)\
    .filter(osc.calculated_at > "2016-08-22")\
    .all()


def gb_obj_from_st_osc_query_tuple(result):
    obj = dict()
    r_osc = result[1]
    obj["last_updated"] = r_osc.calculated_at
    obj["percentage"] = r_osc.percentage
    obj["mark"] = r_osc.mark
    obj["poss_points"] = r_osc.possible_points
    obj["teacher"] = r_osc.gradebook.user.last_name
    obj["range_start"] = r_osc.timeframe_start_date
    obj["range_end"] = r_osc.timeframe_end_date

    return obj

students_dict = dict()

for result in r:
    student = result[0]
    student_id = student.student_id

    if student_id not in students_dict:
        students_dict[student_id] = {
            "first_name": student.first_name,
            "last_name": student.last_name,
            "student_gbs": dict()
        }

    student_gbs = students_dict[student_id]["student_gbs"]

    gb_name = result[1].gradebook.gradebook_name
    if gb_name not in student_gbs:
        student_gbs[gb_name] = gb_obj_from_st_osc_query_tuple(result)

    poss_points = result[1].possible_points
    if poss_points > student_gbs[gb_name]["poss_points"]:
        student_gbs[gb_name] = gb_obj_from_st_osc_query_tuple(result)

s.close()

output = "deanslist_gradebook.csv"
DATE_FORMAT = "%m/%d/%y"

with open(output, "wb") as f:
    writer = csv.writer(f)
    writer.writerow(['Student ID', 'Last Name', 'First Name', 'Teacher',
                     'GradeBook', 'Score Last Updated', 'Percentage',
                     'Mark', 'Grading Period'])
    for id, st in students_dict.items():
        first = st["first_name"]
        last = st["last_name"]
        for gb_name, gb in st["student_gbs"].items():
            last_updated = gb["last_updated"].strftime(DATE_FORMAT)
            if gb["mark"] == ("" or None):
                continue
            grading_period = ("{} - {}".format(gb["range_start"].strftime(DATE_FORMAT),
                                               gb["range_end"].strftime(DATE_FORMAT)))
            row = [id, last, first, gb["teacher"], gb_name, last_updated,
                   gb["percentage"], gb["mark"], grading_period]
            writer.writerow(row)

# send the file via Amazon SES

secrets = json.loads(open("secrets.json", "rb").read())
att_file = open(output, "rb").read()

user = secrets["SES_USER"]
pw = secrets["SES_PW"]
host = secrets["SES_SERVER"]
port = 465
email_from = "apirzada@alphapublicschools.org"
email_to = "apirzada@alphapublicschools.org"
msg = MIMEMultipart()
msg["From"] = email_from
msg["To"] = ", ".join(email_to)
msg["Subject"] = "Deanslist Gradebook"

attachment = MIMEBase('application', 'csv')
attachment.set_payload(att_file)
attachment.add_header('Content-Disposition', 'attachment', filename=output)
Encoders.encode_base64(attachment)
msg.attach(attachment)

s = smtplib.SMTP_SSL(host, port)
s.login(user, pw)
s.sendmail(email_from, email_to, msg.as_string())
s.quit()