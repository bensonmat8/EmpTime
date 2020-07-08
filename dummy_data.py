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


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

    
if __name__=='__main__':
    with app.app_context():
        try:
            dept = Department(dept_id=1, dept_name='Food and Nutrition')
            db.session.add(dept)
            db.session.commit()
        except:
            print('Dept Failed')
        
        try:
            df = pd.read_csv('./Dummy Data/job.csv')
            df.to_sql('job',  db.engine, index=False, if_exists='append')
        except:
            print('Job table failed')
        
        try:
            df = pd.read_csv('./Dummy Data/employee.csv')
            df.to_sql('employee',  db.engine, index=False, if_exists='append')
        except:
            print('Employee table failed')
        
        print('Tables created and dummy data added..')
