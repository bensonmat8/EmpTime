from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()


class Department(db.Model):
    __tablename__ = 'department'
    dept_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String, nullable=False)


class Vacation(db.Model):
    __tablename__ = 'vacation'
    vac_id = db.Column(db.Integer, primary_key=True)
    uniq_id = db.Column(db.String(256),
                        db.ForeignKey('employee.uniq_id'),
                        nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)


class ScheduleSetting(db.Model):
    __tablename__ = 'schedule_setting'
    sch_id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer,
                       db.ForeignKey('job.job_id'),
                       nullable=False)
    job_name = db.Column(db.String, nullable=False)
    shift_start = db.Column(db.Time, nullable=False)
    no_of_emp = db.Column(db.Integer, nullable=False)
    hr_per_shift = db.Column(db.Float, nullable=False)
    comment = db.Column(db.String)
    sub_job_id = db.Column(db.Integer, default=0)
    sun1 = db.Column(db.Integer, default=0)
    mon1 = db.Column(db.Integer, default=0)
    tue1 = db.Column(db.Integer, default=0)
    wed1 = db.Column(db.Integer, default=0)
    thur1 = db.Column(db.Integer, default=0)
    fri1 = db.Column(db.Integer, default=0)
    sat1 = db.Column(db.Integer, default=0)
    sun2 = db.Column(db.Integer, default=0)
    mon2 = db.Column(db.Integer, default=0)
    tue2 = db.Column(db.Integer, default=0)
    wed2 = db.Column(db.Integer, default=0)
    thur2 = db.Column(db.Integer, default=0)
    fri2 = db.Column(db.Integer, default=0)
    sat2 = db.Column(db.Integer, default=0)
    job = db.relationship('Job', backref='schedule_setting')


class Job(db.Model):
    __tablename__ = 'job'
    job_id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String, nullable=False)
    job_group = db.Column(db.String, nullable=True)


class Kitchen_schedule(db.Model):
    __tablename__ = 'kitchen_schedule'
    kitchen_id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String, nullable=True)
    job_id = db.Column(db.Integer, nullable=True)
    job_sub_id = db.Column(db.Integer, nullable=True)
    time = db.Column(db.Time, nullable=True)
    sun1 = db.Column(db.String, nullable=True)
    mon1 = db.Column(db.String, nullable=True)
    tue1 = db.Column(db.String, nullable=True)
    wed1 = db.Column(db.String, nullable=True)
    thur1 = db.Column(db.String, nullable=True)
    fri1 = db.Column(db.String, nullable=True)
    sat1 = db.Column(db.String, nullable=True)
    sun2 = db.Column(db.String, nullable=True)
    mon2 = db.Column(db.String, nullable=True)
    tue2 = db.Column(db.String, nullable=True)
    wed2 = db.Column(db.String, nullable=True)
    thur2 = db.Column(db.String, nullable=True)
    fri2 = db.Column(db.String, nullable=True)
    sat2 = db.Column(db.String, nullable=True)
    hr_per_shift = db.Column(db.Float, nullable=False)
    shift_start = db.Column(db.Time, nullable=False)
    job_group = db.Column(db.String, nullable=True)
    week1date = db.Column(db.Date, nullable=True)


class Employee(db.Model):
    __tablename__ = 'employee'
    uniq_id = db.Column(db.String(256), primary_key=True)
    dept_id = db.Column(db.Integer,
                        db.ForeignKey('department.dept_id'),
                        nullable=False)
    emp_id = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    job_id = db.Column(db.Integer,
                       db.ForeignKey('job.job_id'),
                       nullable=False)
    emp_type = db.Column(db.String, nullable=False)
    shift = db.Column(db.String, nullable=False)
    weekend_off = db.Column(db.Integer, nullable=False)
    week_1_day_off = db.Column(db.String, nullable=False)
    week_2_day_off = db.Column(db.String, nullable=False)
    fte = db.Column(db.Float, nullable=False)
    create_time = db.Column(db.TEXT, nullable=False)
    modify_time = db.Column(db.TEXT, nullable=False)
    create_by = db.Column(db.String, nullable=False)
    modify_by = db.Column(db.String, nullable=False)
    del_ind = db.Column(db.String)
    comment = db.Column(db.String)
    used_fte = db.Column(db.Float, default=0.0)
    used_fte2 = db.Column(db.Float, default=0.0)
    day_check = db.relationship('Day_check', backref='employee')
    vacation = db.relationship('Vacation', backref='employee', lazy=True,
                               order_by='Vacation.end_date')
    job = db.relationship('Job', backref='employee')


class Emp_schedule(db.Model):
    __tablename__ = 'emp_schedule'
    people_id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String,
                       nullable=False)
    emp_name = db.Column(db.String, nullable=True)
    # job_id=db.Column(db.Integer,nullable=True)
    # sub_job_id=db.Column(db.Integer,nullable=True)
    sun1 = db.Column(db.String, nullable=True)
    mon1 = db.Column(db.String, nullable=True)
    tue1 = db.Column(db.String, nullable=True)
    wed1 = db.Column(db.String, nullable=True)
    thur1 = db.Column(db.String, nullable=True)
    fri1 = db.Column(db.String, nullable=True)
    sat1 = db.Column(db.String, nullable=True)
    used_fte = db.Column(db.Float, default=0.0)
    sun2 = db.Column(db.String, nullable=True)
    mon2 = db.Column(db.String, nullable=True)
    tue2 = db.Column(db.String, nullable=True)
    wed2 = db.Column(db.String, nullable=True)
    thur2 = db.Column(db.String, nullable=True)
    fri2 = db.Column(db.String, nullable=True)
    sat2 = db.Column(db.String, nullable=True)
    used_fte2 = db.Column(db.Float, default=0.0)
    total_fte = db.Column(db.Float, default=0.0)
    job_group = db.Column(db.String, nullable=True)
    week1date = db.Column(db.Date, nullable=True)


class Day_check(db.Model):
    __tablename__ = 'day_check'
    matrix_id = db.Column(db.Integer, primary_key=True)
    uniq_id = db.Column(db.String(256),
                        db.ForeignKey('employee.uniq_id'),
                        nullable=False)
    sun1 = db.Column(db.Integer, nullable=True)
    mon1 = db.Column(db.Integer, nullable=True)
    tue1 = db.Column(db.Integer, nullable=True)
    wed1 = db.Column(db.Integer, nullable=True)
    thur1 = db.Column(db.Integer, nullable=True)
    fri1 = db.Column(db.Integer, nullable=True)
    sat1 = db.Column(db.Integer, nullable=True)
    sun2 = db.Column(db.Integer, nullable=True)
    mon2 = db.Column(db.Integer, nullable=True)
    tue2 = db.Column(db.Integer, nullable=True)
    wed2 = db.Column(db.Integer, nullable=True)
    thur2 = db.Column(db.Integer, nullable=True)
    fri2 = db.Column(db.Integer, nullable=True)
    sat2 = db.Column(db.Integer, nullable=True)
    # employee = db.relationship('Employee', backref='day_check')

# --------OccMed App----------------
# Started 2020-09-18


class OccMedCheckIn(db.Model):
    __tablename__ = 'occ_med_checkin'
    checkin_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    campus = db.Column(db.String, nullable=False)
    dept = db.Column(db.String, nullable=False)
    reason = db.Column(db.String, nullable=False)
    comments = db.Column(db.String, nullable=True)
    checkin_time = db.Column(db.DateTime, nullable=False)

# ---------NHSN App----------------------
# Started 2020-09-28


class NHSNdataEntry(db.Model):
    __tablename = 'NHSN_data_entry'
    nhsn_item_id = db.Column(db.String, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    campus = db.Column(db.String, nullable=False)
    unit = db.Column(db.String, nullable=False)
    measure = db.Column(db.String, nullable=False)
    manual_count = db.Column(db.Integer, nullable=True)
    epic_count = db.Column(db.Integer, nullable=True)
    difference = db.Column(db.Integer, nullable=True)
    difference_percent = db.Column(db.Float, nullable=True)
    create_timestamp = db.Column(db.DateTime, nullable=False)
    create_by = db.Column(db.String, nullable=False)
    modify_timestamp = db.Column(db.DateTime, nullable=False)
    modified_by = db.Column(db.String, nullable=False)
    reason_for_change = db.Column(db.String, nullable=True)
    audit = db.Column(db.String, nullable=True)

# ---------COVID Reminder App----------------------
# Started 2021-01-13


class VaccPatReminder(db.Model):
    __tablename__ = 'VaccPatReminder'
    vacc_pat_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=True)
    EmpID = db.Column(db.String, nullable=True)
    vacc_1_date = db.Column(db.DateTime, nullable=False)
    vacc_2_date = db.Column(db.DateTime, nullable=True)
    cell_phone = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    opt_in = db.Column(db.Boolean, nullable=True)
    create_timestamp = db.Column(db.DateTime, nullable=False)
    create_by = db.Column(db.String, nullable=False)
    modify_timestamp = db.Column(db.DateTime, nullable=False)
    modified_by = db.Column(db.String, nullable=False)
    lot = db.Column(db.String, nullable=True)
    ReminderDt_4 = db.Column(db.DateTime, nullable=True)
    ReminderDt_3 = db.Column(db.DateTime, nullable=True)
    ReminderDt_2 = db.Column(db.DateTime, nullable=True)
    ReminderDt_1 = db.Column(db.DateTime, nullable=True)
    ReminderDt0 = db.Column(db.DateTime, nullable=True)
    ReminderDt1 = db.Column(db.DateTime, nullable=True)
    ReminderDt2 = db.Column(db.DateTime, nullable=True)
    ReminderDt3 = db.Column(db.DateTime, nullable=True)
    ReminderDt4 = db.Column(db.DateTime, nullable=True)

# ---------PHC Data Entry----------------------
# Started 2021-02-01


class PHCdataEntry(db.Model):
    __tablename__ = 'PHCdataEntry'
    PHC_id = db.Column(db.String(75), primary_key=True)
    empid = db.Column(db.String(15),
                      # db.ForeignKey('flaskloginusers.empid'),
                      nullable=False)
    date = db.Column(db.Date, nullable=False)
    data_type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)


# ---------User Accounts----------------------
# Started 2021-01-27


class User(UserMixin, db.Model):
    __tablename__ = 'flaskloginusers'
    empid = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=False)
    email = db.Column(db.String(60), nullable=True, unique=True)
    password = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String(15), nullable=False)
    app = db.relationship('UserAppAccess', backref='flaskloginusers')


class UserAppAccess(db.Model):
    __tablename__ = 'user_app_access'
    userappid = db.Column(db.Integer, primary_key=True)
    empid = db.Column(db.String(256),
                      db.ForeignKey('flaskloginusers.empid'),
                      nullable=False)
    appid = db.Column(db.Integer, db.ForeignKey('app_table.appid'),
                      nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String(15), nullable=False)


class AppTable(db.Model):
    __tablename__ = 'app_table'
    appid = db.Column(db.Integer, primary_key=True)
    appName = db.Column(db.String(50), nullable=False, unique=True)
    appRoute = db.Column(db.String(150), nullable=False, unique=True)
