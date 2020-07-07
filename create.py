from flask import Flask, render_template, request
from models import *
import os
import pandas as pd

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def main():
    db.create_all()
    
if __name__=='__main__':
    with app.app_context():
        main()
        try:
            dept = Department(dept_id=1, dept_name='Food and Nutrition')
            db.session.add(dept)
            db.session.commit()
        except:
            pass
        df = pd.read_csv('./Dummy Data/Employee.csv')
        df.to_sql('employee',  db.engine, index=False, if_exists='append')
        print('Tables created and dummy data added..')


