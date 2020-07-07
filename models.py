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
    title = db.Column(db.String, nullable=False)
    shift = db.Column(db.String, nullable=False)
    days_off = db.Column(db.String, nullable=False)
    fte = db.Column(db.Float, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    modify_time =db.Column(db.DateTime, nullable=False)
    create_by = db.Column(db.String, nullable=False)
    modify_by = db.Column(db.String, nullable=False)
    del_ind = db.Column(db.String)
    vacation = db.relationship('Vacation', backref='employee', lazy=True)
    
class Vacation(db.Model):
    __tablename__ = 'vacation'
    vac_id = db.Column(db.Integer, primary_key=True)
    uniq_id = db.Column(db.String,
                        db.ForeignKey('employee.uniq_id'),
                        nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    
# class ScheduleSetting(db.Model):
#     __tablename__ = 'schedule_setting'
#     sch_id = db.Column(db.Integer, primary_key=True)
    
    

# class Job(db.Model):
#     __table__ = 'job'
#     job_id = db.Column(db.Integer, primary_key=True)
#     job_name = db.Column(db.String, nullable=False)
    
