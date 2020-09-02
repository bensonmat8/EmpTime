from flask import Flask, render_template, request
from models import *
from datetime import datetime,timedelta,date
import os
import pandas
from sqlalchemy import or_, and_, func
from sqlalchemy import distinct

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
   
def main():        
    with app.app_context():
        now=datetime.now()
        now=now.replace(microsecond=0)
        db.create_all()      
        Kitchen_schedule.query.delete()
        Day_check.query.delete()
        db.session.commit()
        week=now.isocalendar()[1]
        Emp_schedule.query.delete()
        db.session.commit()
        #use str or time or date based on the type in the database
        p=Vacation.query.all()
        vacation_day=[]
        block_sun1=[]
        block_mon1=[]
        block_tue1=[]
        block_wed1=[]
        block_thur1=[]
        block_fri1=[]
        block_sat1=[]
        block_sun2=[]
        block_mon2=[]
        block_tue2=[]
        block_wed2=[]
        block_thur2=[]
        block_fri2=[]
        block_sat2=[]
        length_v=[] 
        empid=[]
        job_number=Job.query.all()
        jobid=len(job_number)+1
        for value in db.session.query(Employee.first_name,Employee.last_name, Employee.emp_id,Employee.job_id,Employee.uniq_id,Employee.del_ind).distinct(Employee.emp_id):
            empid.append(value)
        for i in range(len(empid)):
            job_group=Job.query.get(empid[i].job_id).job_group
            if empid[i].del_ind!='Y':
                emp_info=Emp_schedule(emp_id=str(empid[i].emp_id),emp_name= empid[i].uniq_id,sun1='-',mon1='-',tue1='-',wed1='-',thur1='-',fri1='-',sat1='-',
                                  sun2='-',mon2='-',tue2='-',wed2='-',thur2='-',fri2='-',sat2='-',job_group=job_group)    
            db.session.add(emp_info)
            db.session.commit()





        for dd in range(len(p)):
            day=(p[dd].end_date-p[dd].start_date).days
            dif = [p[dd].start_date + timedelta(days=x) for x in range((p[dd].end_date-p[dd].start_date).days + 1)]
            vacation_day.append(dif)
            length_v.append(day)
            
        if week%2==0: 
            while now.weekday()!=6:
                now += timedelta(1) 
            all_week=[now.date(),(now+timedelta(days=1)).date(),(now+timedelta(days=2)).date(),(now+timedelta(days=3)).date(),
                        (now+timedelta(days=4)).date(),(now+timedelta(days=5)).date(),
                        (now+timedelta(days=6)).date(),(now+timedelta(days=7)).date(),
                        (now+timedelta(days=8)).date(),(now+timedelta(days=9)).date(),
                        (now+timedelta(days=10)).date(),(now+timedelta(days=11)).date(),
                        (now+timedelta(days=12)).date(),(now+timedelta(days=13)).date()]
            # k_add=Kitchen_schedule(kitchen_id=0,job='Date',job_id=0,job_sub_id=0,time=None,sun1=str(now.date()),mon1=str((now+timedelta(days=1)).date()),tue1=str((now+timedelta(days=2)).date()),wed1=str((now+timedelta(days=3)).date()),
            #                         thur1=str((now+timedelta(days=4)).date()),fri1=str((now+timedelta(days=5)).date()),
            #                         sat1=str((now+timedelta(days=6)).date()),sun2=str((now+timedelta(days=7)).date()),
            #                         mon2=str((now+timedelta(days=8)).date()),tue2=str((now+timedelta(days=9)).date()),
            #                         wed2=str((now+timedelta(days=10)).date()),thur2=str((now+timedelta(days=11)).date()),
            #                         fri2=str((now+timedelta(days=12)).date()),sat2=str((now+timedelta(days=13)).date()),hr_per_shift=0,shift_start=now.time(),job_group='-',week1date=now.date())
            # db.session.add(k_add)
            # db.session.commit()  
        if week%2!=0: 
            while now.weekday()!=6:
                now += timedelta(1)            
            all_week=[(now+timedelta(days=7)).date(),(now+timedelta(days=8)).date(),(now+timedelta(days=9)).date(),(now+timedelta(days=10)).date(),
                        (now+timedelta(days=11)).date(),(now+timedelta(days=12)).date(),
                        (now+timedelta(days=13)).date(),(now+timedelta(days=14)).date(),
                        (now+timedelta(days=15)).date(),(now+timedelta(days=16)).date(),
                        (now+timedelta(days=17)).date(),(now+timedelta(days=18)).date(),
                        (now+timedelta(days=19)).date(),(now+timedelta(days=20)).date()]
            # k_add=Kitchen_schedule(kitchen_id=0,job='Date',job_id=0,job_sub_id=0,time=None,sun1=str((now+timedelta(days=7)).date()),mon1=str((now+timedelta(days=8)).date()),tue1=str((now+timedelta(days=9)).date()),wed1=str((now+timedelta(days=10)).date()),
            #                         thur1=str((now+timedelta(days=11)).date()),fri1=str((now+timedelta(days=12)).date()),
            #                         sat1=str((now+timedelta(days=13)).date()),sun2=str((now+timedelta(days=14)).date()),
            #                         mon2=str((now+timedelta(days=15)).date()),tue2=str((now+timedelta(days=16)).date()),
            #                         wed2=str((now+timedelta(days=17)).date()),thur2=str((now+timedelta(days=18)).date()),
            #                         fri2=str((now+timedelta(days=19)).date()),sat2=str((now+timedelta(days=20)).date()),hr_per_shift=0,shift_start=now.time(),job_group='-',week1date=(now+timedelta(days=7)).date())
            # db.session.add(k_add)
            # db.session.commit()  
        for i in range(len(vacation_day)):
            for j in range(len(all_week)):
                for x in range(length_v[i]+1):
                    if all_week[j]==vacation_day[i][x].date():
                        # print(vacation_day[i][x] for x in range(length_v[i]+1))
                        if all_week[j].weekday()==0 and j<6:
                            block_mon1.append(p[i].uniq_id)
                        if all_week[j].weekday()==1 and j<6:
                            block_tue1.append(p[i].uniq_id)
                        if all_week[j].weekday()==2 and j<6:
                            block_wed1.append(p[i].uniq_id)
                        if all_week[j].weekday()==3 and j<6:
                            block_thur1.append(p[i].uniq_id)
                        if all_week[j].weekday()==4 and j<6:
                            block_fri1.append(p[i].uniq_id)
                        if all_week[j].weekday()==5 and j<6:
                            block_sat1.append(p[i].uniq_id)
                        if all_week[j].weekday()==6 and j==6:
                            block_sun1.append(p[i].uniq_id)
                        if all_week[j].weekday()==0 and j>6:
                            block_mon2.append(p[i].uniq_id)
                        if all_week[j].weekday()==1 and j>5:
                            block_tue2.append(p[i].uniq_id)
                        if all_week[j].weekday()==2 and j>5:
                            block_wed2.append(p[i].uniq_id)
                        if all_week[j].weekday()==3 and j>5:
                            block_thur2.append(p[i].uniq_id)
                        if all_week[j].weekday()==4 and j>5:
                            block_fri2.append(p[i].uniq_id)
                        if all_week[j].weekday()==5 and j>5:
                            block_sat2.append(p[i].uniq_id)
                        if all_week[j].weekday()==6 and j>5:
                            block_sun2.append(p[i].uniq_id)


        empid=[]
        for value in db.session.query(Employee.uniq_id).distinct():
            empid.append(value)
        for i in range(len(empid)):
            emp_add=Day_check(uniq_id=str(empid[i].uniq_id),sun1=0,mon1=0,tue1=0,wed1=0,thur1=0,fri1=0,sat1=0,
                              sun2=0,mon2=0,tue2=0,wed2=0,thur2=0,fri2=0,sat2=0)    
            db.session.add(emp_add)
            db.session.commit()
        job_number=Job.query.all()
        jobid=len(job_number)+1
        emp=Employee.query.all()
        for xx in range(len(emp)):
            emp[xx].used_fte=0
            db.session.commit()
        for j in range(1,jobid):
            job_input=ScheduleSetting.query.filter(ScheduleSetting.job_id==j).all()
            job_group=Job.query.get(j).job_group
            if len(job_input)!=0:
                for i in range(len(job_input)):
                    max_input_emp=max(job_input[i].sun1,job_input[i].mon1,job_input[i].tue1,job_input[i].wed1,
                                      job_input[i].thur1,job_input[i].fri1,job_input[i].sat1,job_input[i].sun2,
                                      job_input[i].mon2,job_input[i].tue2,job_input[i].wed2, job_input[i].thur2,
                                      job_input[i].fri2,job_input[i].sat2)
                    for x in range(max_input_emp):
                        k_add=Kitchen_schedule(job=job_input[i].job_name,job_id=j,job_sub_id=job_input[i].sub_job_id,time=job_input[i].shift_start,sun1='-',mon1='-',tue1='-',wed1='-',thur1='-',fri1='-',sat1='-',
                                          sun2='-',mon2='-',tue2='-',wed2='-',thur2='-',fri2='-',sat2='-',hr_per_shift=job_input[i].hr_per_shift,shift_start=job_input[i].shift_start,job_group=job_group)
                        db.session.add(k_add)
                        db.session.commit()
                    hr_per_shift=ScheduleSetting.query.filter_by(job_id=j, sub_job_id=job_input[i].sub_job_id).all()
                    if hr_per_shift[0].hr_per_shift==8:
                        if job_input[i].sun1!=0:
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Sunday',Employee.emp_type=='Full',Day_check.sun1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_sun1))).order_by(func.random()).limit(job_input[i].mon1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.sun1=1
                                    db.session.commit()        
                            if len(pick_up)!=job_input[i].sun1:
                                left=job_input[i].sun1-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Sunday',Employee.emp_type=='Part',Day_check.sun1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.weekend_off!=1,~Employee.uniq_id.in_(block_sun1))).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up2[n].uniq_id).first()
                                        check.sun1=1
                                        db.session.commit()        
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].sun1=pick_up[n].uniq_id
                                    pick_up[n].used_fte=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.sun1=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].sun1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].sun1):
                                    if sel_schedule[l].sun1 =='-':
                                        sel_schedule[l].sun1="Add_employee"
                                        db.session.commit()
    
                        if job_input[i].mon1!=0:
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Full',Day_check.mon1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_mon1))).order_by(func.random()).limit(job_input[i].mon1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.mon1=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].mon1:
                                left=job_input[i].mon1-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.mon1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_mon1))).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up2[n].uniq_id).first()
                                        check.mon1=1
                                        db.session.commit()
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].mon1=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Full',Day_check.tue1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_tue1))).order_by(func.random()).limit(job_input[i].tue1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.tue1=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].tue1:
                                left=job_input[i].tue1-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.tue1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_tue1))).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up2[n].uniq_id).first()
                                        check.tue1=1
                                        db.session.commit()
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].tue1=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Full',Day_check.wed1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_wed1))).order_by(func.random()).limit(job_input[i].wed1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.wed1=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].wed1:
                                left=job_input[i].wed1-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.wed1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_wed1))).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up2[n].uniq_id).first()
                                        check.wed1=1
                                        db.session.commit()
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].wed1=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Full',Day_check.thur1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_thur1))).order_by(func.random()).limit(job_input[i].thur1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.thur1=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].thur1:
                                left=job_input[i].thur1-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.thur1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_thur1))).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up2[n].uniq_id).first()
                                        check.thur1=1
                                        db.session.commit()
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].thur1=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Full',Day_check.fri1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_fri1))).order_by(func.random()).limit(job_input[i].fri1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.fri1=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].fri1:
                                left=job_input[i].fri1-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.fri1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_fri1))).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up2[n].uniq_id).first()
                                        check.fri1=1
                                        db.session.commit()
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].fri1=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Saturday',Day_check.sat1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Day_check.sun1==0,Employee.weekend_off!=0,~Employee.uniq_id.in_(block_sat1))).order_by(func.random()).limit(job_input[i].sat1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.sat1=1
                                    db.session.commit()                                             
                            if len(pick_up)!=job_input[i].sat1:
                                left=job_input[i].sat1-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Saturday',Employee.emp_type=='Part',Day_check.sat1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.weekend_off!=0,~Employee.uniq_id.in_(block_sat1))).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up2[n].uniq_id).first()
                                        check.sat1=1
                                        db.session.commit()        
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].sat1=pick_up[n].uniq_id
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].sat1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].sat1):
                                    if sel_schedule[l].sat1 =='-':
                                        sel_schedule[l].sat1="Add_employee"
                                        db.session.commit()
                    if hr_per_shift[0].hr_per_shift!=8:
                        if job_input[i].sun1!=0:
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Sunday',Employee.emp_type=='Part',Day_check.sun1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.weekend_off!=1,~Employee.uniq_id.in_(block_sun1))).order_by(func.random()).limit(job_input[i].sun1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.sun1=1
                                    db.session.commit()        
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].sun1=pick_up[n].uniq_id
                                    pick_up[n].used_fte=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].sun1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].sun1):
                                    if sel_schedule[l].sun1 =='-':
                                        sel_schedule[l].sun1="Add_employee"
                                        db.session.commit()
    
                        if job_input[i].mon1!=0:
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.mon1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_mon1))).order_by(func.random()).limit(job_input[i].mon1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.mon1=1
                                    db.session.commit()         
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].mon1=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.tue1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_tue1))).order_by(func.random()).limit(job_input[i].tue1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.tue1=1
                                    db.session.commit()         
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].tue1=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.wed1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_wed1))).order_by(func.random()).limit(job_input[i].wed1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.wed1=1
                                    db.session.commit()         
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].wed1=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.thur1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_thur1))).order_by(func.random()).limit(job_input[i].thur1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.thur1=1
                                    db.session.commit()         
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].thur1=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.fri1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_fri1))).order_by(func.random()).limit(job_input[i].fri1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.fri1=1
                                    db.session.commit()         
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].fri1=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.sat1==0,Day_check.sun1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_sat1))).order_by(func.random()).limit(job_input[i].sat1).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.sat1=1
                                    db.session.commit()         
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].sat1=pick_up[n].uniq_id
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].sat1:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].sat1):
                                    if sel_schedule[l].sat1 =='-':
                                        sel_schedule[l].sat1="Add_employee"
                                        db.session.commit()
    
        emp=Employee.query.all()
        for xx in range(len(emp)):
            emp_fte=Emp_schedule.query.filter(Emp_schedule.emp_id==emp[xx].emp_id).first()
            if emp_fte!=None:
                emp_fte.used_fte=emp[xx].used_fte
            db.session.commit()
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_2_day_off!='Sunday',Employee.emp_type=='Full',Day_check.sun2==0,Day_check.sun1==0,Day_check.sat2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.weekend_off!=0,~Employee.uniq_id.in_(block_sun2))).order_by(func.random()).limit(job_input[i].sun2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.sun2=1
                                    db.session.commit()  
                            if len(pick_up)!=job_input[i].sun2:
                                left=job_input[i].sun2-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_2_day_off!='Sunday',Employee.emp_type=='Part',Day_check.sun2==0,Day_check.sun1==0,Day_check.sat2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.weekend_off!=0,~Employee.uniq_id.in_(block_sun2))).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up2[n].uniq_id).first()
                                        check.sun2=1
                                        db.session.commit()  
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].sun2=pick_up[n].uniq_id
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].sun2:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].sun2):
                                    if sel_schedule[l].sun2 =='-':
                                        sel_schedule[l].sun2="Add_employee"
                                        db.session.commit()
    
                        if job_input[i].mon2!=0:
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Full',Day_check.mon2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_mon2))).order_by(func.random()).limit(job_input[i].mon2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.mon2=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].mon2:
                                left=job_input[i].mon2-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.mon2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_mon2))).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up2[n].uniq_id).first()
                                        check.mon2=1
                                        db.session.commit()
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].mon2=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Full',Day_check.tue2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_tue2))).order_by(func.random()).limit(job_input[i].tue2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.tue2=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].tue2:
                                left=job_input[i].tue2-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.tue2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_tue2))).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up2[n].uniq_id).first()
                                        check.tue2=1
                                        db.session.commit()
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].tue2=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Full',Day_check.wed2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_wed2))).order_by(func.random()).limit(job_input[i].wed2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.wed2=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].wed2:
                                left=job_input[i].wed2-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.wed2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_wed2))).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up2[n].uniq_id).first()
                                        check.wed2=1
                                        db.session.commit()
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].wed2=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Full',Day_check.thur2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_thur2))).order_by(func.random()).limit(job_input[i].thur2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.thur2=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].thur2:
                                left=job_input[i].thur2-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.thur2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_thur2))).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up2[n].uniq_id).first()
                                        check.thur2=1
                                        db.session.commit()
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].thur2=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Full',Day_check.fri2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_fri2))).order_by(func.random()).limit(job_input[i].fri2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.fri2=1
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].fri2:
                                left=job_input[i].fri2-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.fri2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_fri2))).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up2[n].uniq_id).first()
                                        check.fri2=1
                                        db.session.commit()
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].fri2=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_2_day_off!='Saturday',Employee.emp_type=='Full',Day_check.sat2==0,Day_check.sun2==0,Day_check.sat1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.weekend_off!=1,~Employee.uniq_id.in_(block_sat2))).order_by(func.random()).limit(job_input[i].sat2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.sat2=1
                                    db.session.commit()  
                            if len(pick_up)!=job_input[i].sat2:
                                left=job_input[i].sat2-len(pick_up)
                                pick_up2=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_2_day_off!='Saturday',Employee.emp_type=='Part',Day_check.sat2==0,Day_check.sun2==0,Day_check.sat1==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.weekend_off!=1,~Employee.uniq_id.in_(block_sat2))).order_by(func.random()).limit(left).all()
                                if len(pick_up2)!=0:
                                    for n in range(len(pick_up2)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up2[n].uniq_id).first()
                                        check.sat2=1
                                        db.session.commit() 
                                pick_up.extend(pick_up2)
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].sat2=pick_up[n].uniq_id
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
                            pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_2_day_off!='Sunday',Employee.emp_type=='Part',Day_check.sun2==0,Day_check.sun1==0,Day_check.sat2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.weekend_off!=0,~Employee.uniq_id.in_(block_sun2))).order_by(func.random()).limit(job_input[i].sun2).all()
                            if len(pick_up)!=0:
                                for n in range(len(pick_up)):
                                    check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                    check.sun2=1
                                    db.session.commit()  
                            if len(pick_up)!=0:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for n in range(len(pick_up)):
                                    sel_schedule[n].sun2=pick_up[n].uniq_id
                                    new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                    pick_up[n].used_fte=new_hour
                                    db.session.commit()
                            if len(pick_up)!=job_input[i].sun2:
                                sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                for l in range(job_input[i].sun2):
                                    if sel_schedule[l].sun2 =='-':
                                        sel_schedule[l].sun2="Add_employee"
                                        db.session.commit()
    
                            if job_input[i].mon2!=0:
                                pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.mon2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_mon2))).order_by(func.random()).limit(job_input[i].mon2).all()
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                        check.mon2=1
                                        db.session.commit()         
                                if len(pick_up)!=0:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for n in range(len(pick_up)):
                                        sel_schedule[n].mon2=pick_up[n].uniq_id
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
                                pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.tue2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_tue2))).order_by(func.random()).limit(job_input[i].tue2).all()
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                        check.tue2=1
                                        db.session.commit()         
                                if len(pick_up)!=0:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for n in range(len(pick_up)):
                                        sel_schedule[n].tue2=pick_up[n].uniq_id
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
                                pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.wed2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_wed2))).order_by(func.random()).limit(job_input[i].wed2).all()
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                        check.wed2=1
                                        db.session.commit()         
                                if len(pick_up)!=0:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for n in range(len(pick_up)):
                                        sel_schedule[n].wed2=pick_up[n].uniq_id
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
                                pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.thur2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_thur2))).order_by(func.random()).limit(job_input[i].thur2).all()
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                        check.thur2=1
                                        db.session.commit()         
                                if len(pick_up)!=0:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for n in range(len(pick_up)):
                                        sel_schedule[n].thur2=pick_up[n].uniq_id
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
                                pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_1_day_off!='Monday',Employee.emp_type=='Part',Day_check.fri2==0,Day_check.uniq_id==Employee.uniq_id,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,~Employee.uniq_id.in_(block_fri2))).order_by(func.random()).limit(job_input[i].fri2).all()
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                        check.fri2=1
                                        db.session.commit()         
                                if len(pick_up)!=0:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for n in range(len(pick_up)):
                                        sel_schedule[n].fri2=pick_up[n].uniq_id
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
                                pick_up=Employee.query.filter(and_(Employee.del_ind!='Y',Employee.job_id==j,Employee.week_2_day_off!='Saturday',Employee.emp_type=='Part',Day_check.sun2==0,Day_check.sat1==0,Day_check.sat2==0,Employee.fte-Employee.used_fte>=hr_per_shift[0].hr_per_shift,Employee.weekend_off!=1,~Employee.uniq_id.in_(block_sat2))).order_by(func.random()).limit(job_input[i].sat2).all()
                                if len(pick_up)!=0:
                                    for n in range(len(pick_up)):
                                        check=Day_check.query.filter(Day_check.uniq_id==pick_up[n].uniq_id).first()
                                        check.sat2=1
                                        db.session.commit()   
                                if len(pick_up)!=0:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for n in range(len(pick_up)):
                                        sel_schedule[n].sat2=pick_up[n].uniq_id
                                        new_hour=pick_up[n].used_fte+hr_per_shift[0].hr_per_shift
                                        pick_up[n].used_fte=new_hour
                                        db.session.commit()
                                if len(pick_up)!=job_input[i].sat2:
                                    sel_schedule=Kitchen_schedule.query.filter_by(job=job_input[i].job_name, job_sub_id=job_input[i].sub_job_id).all()
                                    for l in range(job_input[i].sat2):
                                        if sel_schedule[l].sat2 =='-':
                                            sel_schedule[l].sat2="Add_employee"
                                            db.session.commit()                                                                                                           
        final_sch=Kitchen_schedule.query.all()
        final_sch_week=Kitchen_schedule.query.all()
        for ff in range(len(final_sch)):
            final_sch[ff].week1date=now
            db.session.commit()
        emp=Employee.query.all()
        for xx in range(len(emp)):
            emp_fte=Emp_schedule.query.filter(Emp_schedule.emp_id==emp[xx].emp_id).first()
            if emp_fte!=None:
                emp_fte.used_fte2=emp[xx].used_fte
            db.session.commit() 
        emp_all=Emp_schedule.query.all()
        for x in range(len(emp_all)):
            emp_all[x].total_fte=emp_all[x].used_fte2+emp_all[x].used_fte
            emp_all[x].week1date=now            
            db.session.commit()

def Emp():
        db.create_all()
        # Emp_schedule.query.delete()
        # db.session.commit()
        # empid=[]
        # for value in db.session.query(Employee.first_name,Employee.last_name, Employee.emp_id).distinct(Employee.emp_id):
        #     empid.append(value)
        # for i in range(len(empid)):
        #     emp_info=Emp_schedule(emp_id=str(empid[i].emp_id),emp_name= empid[i].uniq_id,sun1='-',mon1='-',tue1='-',wed1='-',thur1='-',fri1='-',sat1='-',
        #                       sun2='-',mon2='-',tue2='-',wed2='-',thur2='-',fri2='-',sat2='-')    
        #     db.session.add(emp_info)
        #     db.session.commit()   
        emp_info2=Emp_schedule.query.all()
        for i in range(len(emp_info2)):
            s1=Kitchen_schedule.query.filter(emp_info2[i].emp_name==Kitchen_schedule.sun1).first()
            m1=Kitchen_schedule.query.filter(emp_info2[i].emp_name==Kitchen_schedule.mon1).first()
            t1=Kitchen_schedule.query.filter(emp_info2[i].emp_name==Kitchen_schedule.tue1).first()
            w1=Kitchen_schedule.query.filter(emp_info2[i].emp_name==Kitchen_schedule.wed1).first()
            th1=Kitchen_schedule.query.filter(emp_info2[i].emp_name==Kitchen_schedule.thur1).first()
            f1=Kitchen_schedule.query.filter(emp_info2[i].emp_name==Kitchen_schedule.fri1).first()
            sa1=Kitchen_schedule.query.filter(emp_info2[i].emp_name==Kitchen_schedule.sat1).first()
            s2=Kitchen_schedule.query.filter(emp_info2[i].emp_name==Kitchen_schedule.sun2).first()
            m2=Kitchen_schedule.query.filter(emp_info2[i].emp_name==Kitchen_schedule.mon2).first()
            t2=Kitchen_schedule.query.filter(emp_info2[i].emp_name==Kitchen_schedule.tue2).first()
            w2=Kitchen_schedule.query.filter(emp_info2[i].emp_name==Kitchen_schedule.wed2).first()
            th2=Kitchen_schedule.query.filter(emp_info2[i].emp_name==Kitchen_schedule.thur2).first()
            f2=Kitchen_schedule.query.filter(emp_info2[i].emp_name==Kitchen_schedule.fri2).first()
            sa2=Kitchen_schedule.query.filter(emp_info2[i].emp_name==Kitchen_schedule.sat2).first()
            if s1!=None:
                emp_info2[i].sun1=str(s1.job)+' \n'+str(s1.shift_start)+'-'+str((datetime.combine(date(1, 1, 1), s1.shift_start)+timedelta(hours=s1.hr_per_shift)).time())
            if m1!=None:
                emp_info2[i].mon1=str(m1.job)+' \n'+str(m1.shift_start)+'-'+str((datetime.combine(date(1, 1, 1), m1.shift_start)+timedelta(hours=m1.hr_per_shift)).time())
            if t1!=None:
                emp_info2[i].tue1=str(t1.job)+' \n'+str(t1.shift_start)+'-'+str((datetime.combine(date(1, 1, 1), t1.shift_start)+timedelta(hours=t1.hr_per_shift)).time())
            if w1!=None:
                emp_info2[i].wed1=str(w1.job)+' \n'+str(w1.shift_start)+'-'+str((datetime.combine(date(1, 1, 1), w1.shift_start)+timedelta(hours=w1.hr_per_shift)).time())
            if th1!=None:
                emp_info2[i].thur1=str(th1.job)+' \n'+str(th1.shift_start)+'-'+str((datetime.combine(date(1, 1, 1), th1.shift_start)+timedelta(hours=th1.hr_per_shift)).time())
            if f1!=None:
                emp_info2[i].fri1=str(f1.job)+' \n'+str(f1.shift_start)+'-'+str((datetime.combine(date(1, 1, 1), f1.shift_start)+timedelta(hours=f1.hr_per_shift)).time())
            if sa1!=None:
                emp_info2[i].sat1=str(sa1.job)+' \n'+str(sa1.shift_start)+'-'+str((datetime.combine(date(1, 1, 1), sa1.shift_start)+timedelta(hours=sa1.hr_per_shift)).time())
            if s2!=None:
                emp_info2[i].sun2=str(s2.job)+' \n'+str(s2.shift_start)+'-'+str((datetime.combine(date(1, 1, 1), s2.shift_start)+timedelta(hours=s2.hr_per_shift)).time())
            if m2!=None:
                emp_info2[i].mon2=str(m2.job)+' \n'+str(m2.shift_start)+'-'+str((datetime.combine(date(1, 1, 1), m2.shift_start)+timedelta(hours=m2.hr_per_shift)).time())
            if t2!=None:
                emp_info2[i].tue2=str(t2.job)+' \n'+str(t2.shift_start)+'-'+str((datetime.combine(date(1, 1, 1), t2.shift_start)+timedelta(hours=t2.hr_per_shift)).time())
            if w2!=None:
                emp_info2[i].wed2=str(w2.job)+' \n'+str(w2.shift_start)+'-'+str((datetime.combine(date(1, 1, 1), w2.shift_start)+timedelta(hours=w2.hr_per_shift)).time())
            if th2!=None:
                emp_info2[i].thur2=str(th2.job)+' \n'+str(th2.shift_start)+'-'+str((datetime.combine(date(1, 1, 1), th2.shift_start)+timedelta(hours=th2.hr_per_shift)).time())
            if f2!=None:
                emp_info2[i].fri2=str(f2.job)+' \n'+str(f2.shift_start)+'-'+str((datetime.combine(date(1, 1, 1), f2.shift_start)+timedelta(hours=f2.hr_per_shift)).time())
            if sa2!=None:
                emp_info2[i].sat2=str(sa2.job)+' \n'+str(sa2.shift_start)+'-'+str((datetime.combine(date(1, 1, 1), sa2.shift_start)+timedelta(hours=sa2.hr_per_shift)).time())
            db.session.commit()   

if __name__=='__main__':
    main()