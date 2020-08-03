from flask import Flask, render_template, request
from models import *
from datetime import datetime
import os
import pandas
from sqlalchemy import or_, and_, func

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
   
def main():        
    with app.app_context():
        db.create_all()      
        # Week=['sun1','mon1','tue1','wed1','thur1','fri1','sat1','sun2','mon2','tue2','wed2','thur2','fri2','sat2']
            # s=Kitchen_schedule.query.all()
        job_number=Job.query.all()
        jobid=len(job_number)+1
        emp=Employee.query.all()
        for xx in range(len(emp)):
            emp[xx].used_fte=0
            emp[xx].sun1=0
            emp[xx].sat1=0
            emp[xx].sun2=0
            emp[xx].comment=0
            db.session.commit()
        for j in range(1,jobid):
            job_input=ScheduleSetting.query.filter(ScheduleSetting.job_id==j).all()
            if len(job_input)!=0:
                for i in range(len(job_input)):
                    max_input_emp=max(job_input[i].sun1,job_input[i].mon1,job_input[i].tue1,job_input[i].wed1,
                                      job_input[i].thur1,job_input[i].fri1,job_input[i].sat1,job_input[i].sun2,
                                      job_input[i].mon2,job_input[i].tue2,job_input[i].wed2, job_input[i].thur2,
                                      job_input[i].fri2,job_input[i].sat2)
                    for x in range(max_input_emp):
                        k_add=Kitchen_schedule(job=job_input[i].job_name,job_sub_id=job_input[i].sub_job_id,time=job_input[i].shift_start,sun1='-',mon1='-',tue1='-',wed1='-',thur1='-',fri1='-',sat1='-',
                                         sun2='-',mon2='-',tue2='-',wed2='-',thur2='-',fri2='-',sat2='-')
                        db.session.add(k_add)
                        # db.session.commit()
                        hr_per_shift=ScheduleSetting.query.filter_by(job_id=j, sub_job_id=job_input[i].sub_job_id).all()
                    if hr_per_shift[0].hr_per_shift==8:
                        if job_input[i].sun1!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Sunday',Employee.emp_type=='Full',Employee.comment!='sun1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.weekend_off!=1)).order_by(func.random()).limit(job_input[i].sun1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='sun1'
                            if len(pick_up)!=job_input[i].sun1:
                                left=job_input[i].sun1-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Sunday',Employee.emp_type=='Part',Employee.comment!='sun1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.weekend_off!=1)).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        pick_up2[n].comment='sun1'
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].sun1=pick_up[n].first_name+" "+pick_up[n].last_name
                                    pick_up[n].used_fte=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].sun1=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].sun1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].sun1):
                                    if sel_schedule[l].sun1 =='-':
                                        sel_schedule[l].sun1="Add_employee"
                                        db.session.commit()
    
                        if job_input[i].mon1!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Full',Employee.comment!='mon1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].mon1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='mon1'
                            if len(pick_up)!=job_input[i].mon1:
                                left=job_input[i].mon1-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='mon1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        pick_up2[n].comment='mon1'
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].mon1=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].mon1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].mon1):
                                    if sel_schedule[l].mon1 =='-':
                                        sel_schedule[l].mon1="Add_employee"
                                        db.session.commit()
    
                        if job_input[i].tue1!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Full',Employee.comment!='tue1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].tue1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='tue1'
                            if len(pick_up)!=job_input[i].tue1:
                                left=job_input[i].tue1-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='tue1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        pick_up2[n].comment='tue1'
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].tue1=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].tue1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].tue1):
                                    if sel_schedule[l].tue1 =='-':
                                        sel_schedule[l].tue1="Add_employee"
                                        db.session.commit()
    
                        if job_input[i].wed1!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Full',Employee.comment!='wed1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].wed1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='wed1'
                            if len(pick_up)!=job_input[i].wed1:
                                left=job_input[i].wed1-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='wed1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        pick_up2[n].comment='wed1'
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].wed1=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].wed1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].wed1):
                                    if sel_schedule[l].wed1 =='-':
                                        sel_schedule[l].wed1="Add_employee"
                                        db.session.commit()
    
                                    
                        if job_input[i].thur1!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Full',Employee.comment!='thur1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].thur1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='thur1'
                            if len(pick_up)!=job_input[i].thur1:
                                left=job_input[i].thur1-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='thur1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        pick_up2[n].comment='thur1'
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].thur1=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].thur1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].thur1):
                                    if sel_schedule[l].thur1 =='-':
                                        sel_schedule[l].thur1="Add_employee"
                                        db.session.commit()
    
                        if job_input[i].fri1!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Full',Employee.comment!='fri1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].fri1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='fri1'
                            if len(pick_up)!=job_input[i].fri1:
                                left=job_input[i].fri1-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='fri1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        pick_up2[n].comment='fri1'
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].fri1=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].fri1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].fri1):
                                    if sel_schedule[l].fri1 =='-':
                                        sel_schedule[l].fri1="Add_employee"
                                        db.session.commit()
    
                        if job_input[i].sat1!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Saturday',Employee.emp_type=='Full',Employee.comment!='sat1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.sun1==0,Employee.weekend_off!=0)).order_by(func.random()).limit(job_input[i].sat1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='sat1'                      
                            if len(pick_up)!=job_input[i].sat1:
                                left=job_input[i].sat1-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Saturday',Employee.emp_type=='Part',Employee.comment!='sat1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.sun1==0,Employee.weekend_off!=0)).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        pick_up2[n].comment='sat1'
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].sat1=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    pick_up[n].sat1=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].sat1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].sat1):
                                    if sel_schedule[l].sat1 =='-':
                                        sel_schedule[l].sat1="Add_employee"
                                        db.session.commit()
                    if hr_per_shift[0].hr_per_shift!=8:
                        if job_input[i].sun1!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Sunday',Employee.emp_type=='Part',Employee.comment!='sun1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.weekend_off!=1)).order_by(func.random()).limit(job_input[i].sun1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='sun1'
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].sun1=pick_up[n].first_name+" "+pick_up[n].last_name
                                    pick_up[n].used_fte=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].sun1=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].sun1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].sun1):
                                    if sel_schedule[l].sun1 =='-':
                                        sel_schedule[l].sun1="Add_employee"
                                        db.session.commit()

                        if job_input[i].mon1!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='mon1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].mon1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='mon1'
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].mon1=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].mon1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].mon1):
                                    if sel_schedule[l].mon1 =='-':
                                        sel_schedule[l].mon1="Add_employee"
                                        db.session.commit()

                        if job_input[i].tue1!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='tue1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].tue1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='tue1'
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].tue1=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].tue1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].tue1):
                                    if sel_schedule[l].tue1 =='-':
                                        sel_schedule[l].tue1="Add_employee"
                                        db.session.commit()

                        if job_input[i].wed1!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='wed1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].wed1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='wed1'
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].wed1=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].wed1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].wed1):
                                    if sel_schedule[l].wed1 =='-':
                                        sel_schedule[l].wed1="Add_employee"
                                        db.session.commit()
                        if job_input[i].thur1!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='thur1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].thur1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='thur1'
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].thur1=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].thur1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].thur1):
                                    if sel_schedule[l].thur1 =='-':
                                        sel_schedule[l].thur1="Add_employee"
                                        db.session.commit()
                        if job_input[i].fri1!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='fri1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].fri1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='fri1'
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].fri1=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].fri1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].fri1):
                                    if sel_schedule[l].fri1 =='-':
                                        sel_schedule[l].fri1="Add_employee"
                                        db.session.commit()
                        if job_input[i].sat1!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_1_day_off!='Saturday',Employee.emp_type=='Part',Employee.comment!='sat1',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.sun1==0,Employee.weekend_off!=0)).order_by(func.random()).limit(job_input[i].sat1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='sat1'                      
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].sat1=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    pick_up[n].sat1=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].sat1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].sat1):
                                    if sel_schedule[l].sat1 =='-':
                                        sel_schedule[l].sat1="Add_employee"
                                        db.session.commit()                        
        emp=Employee.query.all()
        for xx in range(len(emp)):
            emp[xx].used_fte=0
            db.session.commit()
        for j in range(1,jobid):
            job_input=ScheduleSetting.query.filter(ScheduleSetting.job_id==j).all()
            if len(job_input)!=0:
                for i in range(len(job_input)):
                    hr_per_shift=ScheduleSetting.query.filter_by(job_id=j, sub_job_id=job_input[i].sub_job_id).all()
                    if hr_per_shift[0].hr_per_shift==8:
                        if job_input[i].sun2!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Sunday',Employee.emp_type=='Full',Employee.comment!='sun2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.sun1==0,Employee.weekend_off!=0)).order_by(func.random()).limit(job_input[i].sun2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='sun2'                      
                            if len(pick_up)!=job_input[i].sun2:
                                left=job_input[i].sun2-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Sunday',Employee.emp_type=='Part',Employee.comment!='sun2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.sun1==0,Employee.weekend_off!=0)).order_by(func.random()).limit(left).all()
                                pick_up.extend(pick_up2)
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        pick_up[n].comment='sun2'                      
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].sun2=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    pick_up[n].sun2=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].sun2:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].sun2):
                                    if sel_schedule[l].sun2 =='-':
                                        sel_schedule[l].sun2="Add_employee"
                                        db.session.commit()
    
                        if job_input[i].mon2!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Monday',Employee.emp_type=='Full',Employee.comment!='mon2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].mon2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='mon2'                      
                            if len(pick_up)!=job_input[i].mon2:
                                left=job_input[i].mon2-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='mon2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(left).all()
                                pick_up.extend(pick_up2)
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        pick_up[n].comment='mon2'                                                  
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].mon2=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].mon2:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].mon2):
                                    if sel_schedule[l].mon2 =='-':
                                        sel_schedule[l].mon2="Add_employee"
                                        db.session.commit()
    
                        if job_input[i].tue2!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Monday',Employee.emp_type=='Full',Employee.comment!='tue2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].tue2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='tue2'                      
                            if len(pick_up)!=job_input[i].tue2:
                                left=job_input[i].tue2-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='tue2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(left).all()
                                pick_up.extend(pick_up2)
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        pick_up[n].comment='tue2'                                                  
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].tue2=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].tue2:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].tue2):
                                    if sel_schedule[l].tue2 =='-':
                                        sel_schedule[l].tue2="Add_employee"
                                        db.session.commit()
    
                        if job_input[i].wed2!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Monday',Employee.emp_type=='Full',Employee.comment!='wed2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].wed2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='wed2'                      
                            if len(pick_up)!=job_input[i].wed2:
                                left=job_input[i].wed2-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='wed2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(left).all()
                                pick_up.extend(pick_up2)
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        pick_up[n].comment='wed2'                                                  
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].wed2=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].wed2:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].wed2):
                                    if sel_schedule[l].wed2 =='-':
                                        sel_schedule[l].wed2="Add_employee"
                                        db.session.commit()
    
                        if job_input[i].thur2!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Monday',Employee.emp_type=='Full',Employee.comment!='thur2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].thur2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='thur2'                      
                            if len(pick_up)!=job_input[i].thur2:
                                left=job_input[i].thur2-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='thur2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(left).all()
                                pick_up.extend(pick_up2)
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        pick_up[n].comment='thur2'                                                  
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].thur2=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].thur2:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].thur2):
                                    if sel_schedule[l].thur2 =='-':
                                        sel_schedule[l].thur2="Add_employee"
                                        db.session.commit()
    
                        if job_input[i].fri2!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Monday',Employee.emp_type=='Full',Employee.comment!='fri2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].fri2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='fri2'                      
                            if len(pick_up)!=job_input[i].fri2:
                                left=job_input[i].fri2-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='fri2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(left).all()
                                pick_up.extend(pick_up2)
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        pick_up[n].comment='fri2'                                                  
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].fri2=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].fri2:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].fri2):
                                    if sel_schedule[l].fri2 =='-':
                                        sel_schedule[l].fri2="Add_employee"
                                        db.session.commit()
    
                        if job_input[i].sat2!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Saturday',Employee.emp_type=='Full',Employee.comment!='sat2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.sat1==0,Employee.sun2==0,Employee.weekend_off!=1)).order_by(func.random()).limit(job_input[i].sat2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='sat2'                      
                            if len(pick_up)!=job_input[i].sat2:
                                left=job_input[i].sat2-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Saturday',Employee.emp_type=='Part',Employee.comment!='sat2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.sat1==0,Employee.sun2==0,Employee.weekend_off!=1)).order_by(func.random()).limit(left).all()
                                pick_up.extend(pick_up2)
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        pick_up[n].comment='sat2'                      
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].sat2=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].sat2:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].sat2):
                                    if sel_schedule[l].sat2 =='-':
                                        sel_schedule[l].sat2="Add_employee"
                                        db.session.commit()
                    if hr_per_shift[0].hr_per_shift!=8:
                       if job_input[i].sun2!=0:
                            pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Sunday',Employee.emp_type=='Part',Employee.comment!='sun2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.sun1==0,Employee.weekend_off!=0)).order_by(func.random()).limit(job_input[i].sun2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    pick_up[n].comment='sun2'                                           
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].sun2=pick_up[n].first_name+" "+pick_up[n].last_name
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    pick_up[n].sun2=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].sun2:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].sun2):
                                    if sel_schedule[l].sun2 =='-':
                                        sel_schedule[l].sun2="Add_employee"
                                        db.session.commit()

                            if job_input[i].mon2!=0:
                                pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='mon2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].mon2).all()
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        pick_up[n].comment='mon2'                                                                       
                                if len(pick_up)!=0:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for n in range(len(pick_up)):
                                        sel_schedule[n].mon2=pick_up[n].first_name+" "+pick_up[n].last_name
                                        new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                        pick_up[n].used_fte=new_hour
                                        db.session.commit()
                                if len(pick_up)!=job_input[i].mon2:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for l in range(job_input[i].mon2):
                                        if sel_schedule[l].mon2 =='-':
                                            sel_schedule[l].mon2="Add_employee"
                                            db.session.commit()

                            if job_input[i].tue2!=0:
                                pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='tue2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].tue2).all()
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        pick_up[n].comment='tue2'                                                                       
                                if len(pick_up)!=0:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for n in range(len(pick_up)):
                                        sel_schedule[n].tue2=pick_up[n].first_name+" "+pick_up[n].last_name
                                        new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                        pick_up[n].used_fte=new_hour
                                        db.session.commit()
                                if len(pick_up)!=job_input[i].tue2:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for l in range(job_input[i].tue2):
                                        if sel_schedule[l].tue2 =='-':
                                            sel_schedule[l].tue2="Add_employee"
                                            db.session.commit()
                                                                        
                            if job_input[i].wed2!=0:
                                pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='wed2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].wed2).all()
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        pick_up[n].comment='wed2'                                                                       
                                if len(pick_up)!=0:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for n in range(len(pick_up)):
                                        sel_schedule[n].wed2=pick_up[n].first_name+" "+pick_up[n].last_name
                                        new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                        pick_up[n].used_fte=new_hour
                                        db.session.commit()
                                if len(pick_up)!=job_input[i].wed2:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for l in range(job_input[i].wed2):
                                        if sel_schedule[l].wed2 =='-':
                                            sel_schedule[l].wed2="Add_employee"
                                            db.session.commit()
                                   
                            if job_input[i].thur2!=0:
                                pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='thur2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].thur2).all()
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        pick_up[n].comment='thur2'                                                                       
                                if len(pick_up)!=0:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for n in range(len(pick_up)):
                                        sel_schedule[n].thur2=pick_up[n].first_name+" "+pick_up[n].last_name
                                        new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                        pick_up[n].used_fte=new_hour
                                        db.session.commit()
                                if len(pick_up)!=job_input[i].thur2:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for l in range(job_input[i].thur2):
                                        if sel_schedule[l].thur2 =='-':
                                            sel_schedule[l].thur2="Add_employee"
                                            db.session.commit()
                            if job_input[i].fri2!=0:
                               pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Monday',Employee.emp_type=='Part',Employee.comment!='fri2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift)).order_by(func.random()).limit(job_input[i].fri2).all()
                               if len(pick_up)!=0:
                                   for n in range(len(pick_up)):
                                       pick_up[n].comment='fri2'                                                                       
                               if len(pick_up)!=0:
                                   sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                   for n in range(len(pick_up)):
                                       sel_schedule[n].fri2=pick_up[n].first_name+" "+pick_up[n].last_name
                                       new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                       pick_up[n].used_fte=new_hour
                                       db.session.commit()
                               if len(pick_up)!=job_input[i].fri2:
                                   sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                   for l in range(job_input[i].fri2):
                                       if sel_schedule[l].fri2 =='-':
                                           sel_schedule[l].fri2="Add_employee"
                                           db.session.commit()
                            if job_input[i].sat2!=0:
                                pick_up=Employee.query.filter(and_(Employee.job_id==j,Employee.week_2_day_off!='Saturday',Employee.emp_type=='Part',Employee.comment!='sat2',Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.sat1==0,Employee.sun2==0,Employee.weekend_off!=1)).order_by(func.random()).limit(job_input[i].sat2).all()
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        pick_up[n].comment='sat2'                                            
                                if len(pick_up)!=0:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for n in range(len(pick_up)):
                                        sel_schedule[n].sat2=pick_up[n].first_name+" "+pick_up[n].last_name
                                        new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                        pick_up[n].used_fte=new_hour
                                        db.session.commit()
                                if len(pick_up)!=job_input[i].sat2:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for l in range(job_input[i].sat2):
                                        if sel_schedule[l].sat2 =='-':
                                            sel_schedule[l].sat2="Add_employee"
                                            db.session.commit()                                                                                                           
                # db.create_all()
if __name__=='__main__':
    main()