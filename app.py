"""
Created on Sun Jun 21 20:22:05 2020

@author: bensonshajimathew
"""
from flask import Flask, render_template, request
from models import *
from datetime import datetime
import os
import pandas
from sqlalchemy import or_, and_, func

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile('config.py')
db.init_app(app)

with app.app_context():
    dept = {i.dept_name:i.dept_id for i in Department.query.all()}

@app.route('/Home')
def index():
    
    return render_template('hello.html')

@app.route('/GeneralSettings')
def general_settings():
    return render_template('GeneralSettings.html')

@app.route('/EmpSearch', methods=['GET','POST'])
def EmpSearch():
    emp_dtl = request.form.get('emp_dtl')
    if emp_dtl != None:
        #print('EmpSearch if stmt..')
        emp_dtl_f = func.lower(f'%{emp_dtl}%')
        emp_list = Employee.query.filter(or_(
            func.lower(Employee.first_name).like(emp_dtl_f),
            func.lower(Employee.last_name).like(emp_dtl_f),
            func.lower(Employee.emp_id).like(emp_dtl_f))
            ).order_by(Employee.first_name)
        
    else:
        #print('EmpSearch else stmt..')
        emp_list = Employee.query.order_by(Employee.first_name).all()
        
    return render_template('EmpSearch.html', items=emp_list)

@app.route('/employee')
def employee():
    global dept
    job = Job.query.order_by(Job.job_name).all()
    return render_template("EmployeePage.html", dept=dept, submit=None,
                           update='hidden', dt=None, del_ind=None, job=job)
@app.route('/Schedule')
def schedule():
    
    return render_template('Schedule.html')

@app.route('/EmployeeEdit/<uniq_id>', methods=['GET', 'POST'])
def employee_edit(uniq_id):
    dt = Employee.query.get(uniq_id)
    vac = dt.vacation
    if dt.del_ind.lower()=='n':
        del_ind = None
    else:
        del_ind = 'checked=checked'
    job = Job.query.order_by(Job.job_name).all()
    return render_template("EmployeePage.html", dept=dept, submit='hidden',
                           update=None, dt=dt, del_ind=del_ind, vac=vac, job=job)
    
@app.route('/employeesubmit', methods=['GET','POST'])
def emp_submit():
    if request.method == 'GET':
        return 'Please submit the form.'
    e_num = request.form.get('e_num')
    dept_id = request.form.get('dept_id')
    dept_id = dept[dept_id]
    last = request.form.get('last')
    first = request.form.get('first')
    title = request.form.get('job_title')
    shift = request.form.get('shift')
    fte = request.form.get('fte')
    days_off = request.form.getlist('days_off')
    print(days_off)
    if request.form.get('del_ind'): 
         del_ind = 'Y'
    else:
        del_ind = 'n'
    if request.form.get('update')==None:
        emp_add = Employee(uniq_id=str(dept_id)+e_num, dept_id=dept_id,
                           emp_id=e_num, first_name=first, last_name=last,
                           title=title, shift=shift, days_off=days_off,
                           fte=fte, create_time=datetime.now(),
                           modify_time=datetime.now(), create_by='Admin',
                           modify_by='Admin', del_ind=del_ind)
        db.session.add(emp_add)
        result = 'success'
    else:
        
        emp_update = Employee.query.get(str(dept_id)+e_num)
        emp_update.dept_id = dept_id
        emp_update.emp_id = e_num
        emp_update.first_name = first
        emp_update.last_name = last
        emp_update.title = title
        emp_update.shift = shift
        emp_update.days_off = days_off[0]
        emp_update.fte = fte
        emp_update.modify_time = datetime.now()
        emp_update.modify_by = 'Admin'
        emp_update.del_ind = del_ind
        result = 'success'
        
    db.session.commit()
    if result == 'success':
        return render_template('EmployFormSubmit.html', name=last+', '+first)
    else:
        return render_template('SubmitError.html', name=last+', '+first,
                               result=result)



@app.route('/employee/vacation/<uniq_id>', methods=['GET', 'POST'])
def vacation(uniq_id):
    
    emp = Employee.query.get(uniq_id)
    date=datetime.now()
    return render_template('Vacation.html', employee=emp, date=date.strftime('%m/%d/%Y'))

@app.route('/employee/vacationsubmit', methods=['GET','POST'])
def vac_submit():
    # print('Vacation update start')
    uniq_id = request.form.get('uniq_id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    # print(f'Unq id: {uniq_id}')
    vac = Vacation(uniq_id=uniq_id, start_date=start_date, end_date=end_date,
                   create_time=datetime.now())
    db.session.add(vac)
    db.session.commit()
    # print('Vacation update stop')
    result = 'vacation'
    return render_template('Submit.html', result=result)

@app.route('/employee/VacDel/<vac_id>')
def vac_del(vac_id):
    vac = Vacation.query.get(vac_id)
    dt = vac.employee
    db.session.delete(vac)
    db.session.commit()
    vac = dt.vacation
    if dt.del_ind.lower()=='n':
        del_ind = None
    else:
        del_ind = 'checked=checked'
    return render_template("EmployeePage.html", dept=dept, submit='hidden',
                           update=None, dt=dt, del_ind=del_ind, vac=vac)

@app.route('/ScheduleSetting')
def schedule_setting():
    job = Job.query.order_by(Job.job_name).all()
    return render_template('ScheduleSetting.html', job=job)

@app.route('/ScheduleSetting/Submit', methods=['GET','POST'])
def schedule_setting_submit():
    job = request.form.get('job')
    shift_start = request.form.get('shift_start')
    no_of_emp = request.form.get('no_of_emp')
    hr_per_shift = request.form.get('hr_per_shift')
    
    
    sch = ScheduleSetting(job_id=job, shift_start=shift_start,
                          no_of_emp=no_of_emp, hr_per_shift=hr_per_shift)
    db.session.add(sch)
    job_opt = Job.query.order_by(Job.job_name).all()
    return render_template('ScheduleSetting.html', job=job_opt)


