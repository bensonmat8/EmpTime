from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = 'department'
    dept_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String, nullable=False)
    
class Employee(db.Model):
    __tablename__ = 'employee'
    uniq_id = db.Column(db.String, primary_key=True)
    dept_id = db.Column(db.Integer,
                        db.ForeignKey('department.dept_id'),
                        nullable=False)
    emp_id = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    job_id = db.Column(db.Integer,
                       db.ForeignKey('job.job_id'),
                       nullable=False)
    shift = db.Column(db.String, nullable=False)
    weekend_off = db.Column(db.Integer, nullable=False)
    week_1_day_off = db.Column(db.String)
    week_2_day_off = db.Column(db.String)
    fte = db.Column(db.Float, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    modify_time =db.Column(db.DateTime, nullable=False)
    create_by = db.Column(db.String, nullable=False)
    modify_by = db.Column(db.String, nullable=False)
    del_ind = db.Column(db.String)
    comment = db.Column(db.String)
    used_fte = db.Column(db.Float, default=0.0)
    Sun1 = db.Column(db.Integer, default=0)
    Sun2 = db.Column(db.Integer, default=0)
    Sat1 = db.Column(db.Integer, default=0)
    vacation = db.relationship('Vacation', backref='employee', lazy=True,
                               order_by='Vacation.end_date')
    job = db.relationship('Job', backref='employee')
    
class Vacation(db.Model):
    __tablename__ = 'vacation'
    vac_id = db.Column(db.Integer, primary_key=True)
    uniq_id = db.Column(db.String,
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
    hr_per_shift = db.Column(db.Integer, nullable=False)
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
    
class Kitchen_schedule(db.Model):
    __tablename__ = 'Kitchen_schedule'
    Job = db.Column(db.Integer, primary_key=True)
    Time = db.Column(db.String, nullable=False)
    Sun1 = db.Column(db.String, nullable=False)
    Mon1 = db.Column(db.String, nullable=False)
    Tue1 = db.Column(db.String, nullable=False)
    Wed1 = db.Column(db.String, nullable=False)    
    Thur1 = db.Column(db.String, nullable=False)    
    Fri1 = db.Column(db.String, nullable=False)
    Sat1 = db.Column(db.String, nullable=False)
    Sun2 = db.Column(db.String, nullable=False)
    Mon2 = db.Column(db.String, nullable=False)
    Tue2 = db.Column(db.String, nullable=False)
    Wed2 = db.Column(db.String, nullable=False)   
    Thur2 = db.Column(db.String, nullable=False)
    Fri2 = db.Column(db.String, nullable=False)
    Sat2 = db.Column(db.String, nullable=False)
    
    
    
    
    