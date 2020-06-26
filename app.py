#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 20:22:05 2020

@author: bensonshajimathew
"""
from flask import Flask, render_template, request
from models import *
from datetime import datetime
import os
import pandas

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile('config.py')
db.init_app(app)

with app.app_context():
    dept = {i.dept_name:i.dept_id for i in Department.query.all()}

@app.route('/Home')
def index():
    
    return render_template('hello.html')

@app.route('/EmpSearch', methods=['GET','POST'])
def EmpSearch():
    emp_dtl = request.form.get('emp_dtl')
    if emp_dtl != None:
        #print('EmpSearch if stmt..')
        emp_list = Employee.query.filter(or_(Employee.first_name.like(f'%%'),
                                             Employee.last_name.like(f'%%'),
                                             Employee.emp_id.like(f'%%')
                                             )).all()
    else:
        #print('EmpSearch else stmt..')
        emp_list = Employee.query.order_by(Employee.first_name).all()
        
    return render_template('EmpSearch.html', items=emp_list)

@app.route('/employee')
def employee():
    global dept
    return render_template("EmployeePage.html", dept=dept, submit=None,
                           update='hidden', dt=None, del_ind=None)
@app.route('/Schedule')
def schedule():
    
    return render_template('Schedule.html')

@app.route('/EmployeeEdit/<uniq_id>', methods=['GET', 'POST'])
def employee_edit(uniq_id):
    dt = Employee.query.get(uniq_id)
    if dt.del_ind.lower()=='n':
        del_ind = None
    else:
        del_ind = 'checked=checked'
    return render_template("EmployeePage.html", dept=dept, submit='hidden',
                           update=None, dt=dt, del_ind=del_ind)
    
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














