#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 23:49:52 2020

@author: bensonshajimathew
"""

from flask import Flask, render_template, request
from models import *
import os
import pandas as pd
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
engine = create_engine(SQLALCHEMY_DATABASE_URI)

if __name__ == '__main__':
    with app.app_context():
        try:
            dept = Department(dept_id=1, dept_name='Food and Nutrition')
            db.session.add(dept)
            db.session.commit()
            print('Dept Table Added')
        except:
            print('Dept Failed')

        try:
            conn = engine.connect()
            try:
                conn.execute('set IDENTITY_INSERT dbo.job ON')
            except:
                pass
            df = pd.read_csv('./Dummy Data/job.csv')
            df.to_sql('job',  conn, index=False, if_exists='append')
            conn.execute(
                """SELECT pg_catalog.setval(pg_get_serial_sequence('job', 'job_id'), (SELECT MAX(job_id) FROM job)+1);""")
            conn.execute("""UPDATE job SET job_group = 'Cook' WHERE job_name in ('Cook');
UPDATE job SET job_group = 'Retail' WHERE job_name in ('Retail');
UPDATE job SET job_group = 'Diet' WHERE job_name in ('Diet');
UPDATE job SET job_group = 'Kitchen' WHERE job_name in ('Builder', 'Cold Prep', 'Disher/Pots', 'Dishroom', 'Floor Stock', 'RSA', 'Training');
""")
            conn.close()
            print('Job Table Added')
        except:
            print('Job table failed')

        try:
            conn = engine.connect()
            try:
                conn.execute('set IDENTITY_INSERT dbo.employee ON')
            except:
                pass
            df = pd.read_csv('./Dummy Data/employee.csv')
            df.to_sql('employee',  conn, index=False, if_exists='append')
            conn.close()
            print('Employee Table Added')
        except:
            print('Employee table failed')
        try:
            conn = engine.connect()
            try:
                conn.execute('set IDENTITY_INSERT dbo.schedule_setting ON')
            except:
                pass
            df = pd.read_csv('./Dummy Data/schedule_setting.csv')
            df.to_sql('schedule_setting',  conn,
                      index=False, if_exists='append')
            conn.execute(
                "SELECT pg_catalog.setval(pg_get_serial_sequence('schedule_setting', 'sch_id'), (SELECT MAX(sch_id) FROM schedule_setting)+1);")
            conn.close()
            print('Schedule_setting Table Added')
        except:
            print('schedule_setting table failed')
        try:
            conn = engine.connect()
            try:
                conn.execute('set IDENTITY_INSERT dbo.vacation ON')
            except:
                pass
            df = pd.read_csv('./Dummy Data/vacation.csv')
            df.to_sql('vacation',  conn, index=False, if_exists='append')
            conn.execute(
                "SELECT pg_catalog.setval(pg_get_serial_sequence('vacation', 'vac_id'), (SELECT MAX(vac_id) FROM vacation)+1);")
            conn.close()
            print('Vacation Table Added')
        except:
            print('vacation table failed')

        print('Complete..')
