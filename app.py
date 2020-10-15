"""
Created on Sun Jun 21 20:22:05 2020

@author: bensonshajimathew
"""
import json
from flask import Flask, render_template, request, jsonify, Response
from models import *
from datetime import datetime, timedelta
import os
import threading
import time
import pandas as pd
from sqlalchemy import or_, and_, func
import re
SQL_OPERATORS = re.compile('SELECT|UPDATE|INSERT|DELETE', re.IGNORECASE)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile('config.py')
db.init_app(app)


def dataDump(backupKill):
    backupKill = 'True'
    ticker = threading.Event()
    while True:
        with open('backupKill.txt', 'r') as f:
            backupKill = f.read()
        table = pd.read_sql_table('nhs_ndata_entry', db.engine)
    time.sleep()
# with app.app_context():
#     dept = {i.dept_name: i.dept_id for i in Department.query.all()}


# @app.route("/")
# def hello():
#     return "Testing ..."


@app.route('/Home')
def index():

    return render_template('hello.html')


@app.route('/GeneralSettings')
def general_settings():
    return render_template('GeneralSettings.html')


@app.route('/EmpSearch', methods=['GET', 'POST'])
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
    dept = Department.query.all()
    job = Job.query.order_by(Job.job_name).all()
    return render_template("EmployeePage.html", dept=dept, submit=None,
                           update='hidden', dt=None, del_ind=None, job=job)


@app.route('/Schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        import operation
        operation.main()
    emp_dtl = request.form.get('emp_dtl')
    if emp_dtl != None:
        #print('EmpSearch if stmt..')
        emp_dtl_f = func.lower(f'%{emp_dtl}%')
        emp_list = Kitchen_schedule.query.filter(or_(
            func.lower(Kitchen_schedule.Job).like(emp_dtl_f),
            func.lower(Kitchen_schedule.Sun1).like(emp_dtl_f),
            func.lower(Kitchen_schedule.Mon1).like(emp_dtl_f))
        ).order_by(Kitchen_schedule.kitchen_id)

    else:
        #print('EmpSearch else stmt..')
        emp_list = Kitchen_schedule.query.order_by(
            Kitchen_schedule.kitchen_id).all()
    emp = Employee.query.order_by(Employee.uniq_id).all()
    return render_template('Schedule.html', items=emp_list, emp=emp)

# test


@app.route('/EmpSchedule', methods=['GET', 'POST'])
def emp_table():
    import operation
    operation.Emp()

    # emp_dtl = request.form.get('emp_dtl')
    # if emp_dtl != None:
    #     #print('EmpSearch if stmt..')
    #     emp_dtl_f = func.lower(f'%{emp_dtl}%')
    #     emp_list = Emp_schedule.query.filter(or_(
    #         func.lower(Emp_schedule.emp_name).like(emp_dtl_f),
    #         func.lower(Emp_schedule.sun1).like(emp_dtl_f),
    #         func.lower(Emp_schedule.mon1).like(emp_dtl_f))
    #         ).order_by(Emp_schedule.people_id)

    # else:
    #print('EmpSearch else stmt..')
    emp_list = Emp_schedule.query.order_by(Emp_schedule.emp_name).all()
    return render_template('EmpSchedule.html', items=emp_list)


@app.route('/EmployeeEdit/<uniq_id>', methods=['GET', 'POST'])
def employee_edit(uniq_id):
    dept = Department.query.all()
    dt = Employee.query.get(uniq_id)
    vac = dt.vacation
    if dt.del_ind == 'Y':
        del_ind = 'checked=checked'
    else:
        del_ind = None
    job = Job.query.order_by(Job.job_name).all()
    #print(f'week_1_day_off for emp: {dt.week_1_day_off}')
    return render_template("EmployeePage.html", dept=dept, submit='hidden',
                           update=None, dt=dt, del_ind=del_ind, vac=vac, job=job)


@app.route('/employeesubmit', methods=['GET', 'POST'])
def emp_submit():
    if request.method == 'GET':
        return 'Please submit the form.'
    e_num = request.form.get('e_num')
    #print(f'Enum: {e_num}')
    dept_id = request.form.get('dept_id')
    dept_id = dept_id
    #print(f'Department Id: {dept_id}')
    last = request.form.get('last')
    first = request.form.get('first')
    #print(f'First Name : {first}')
    job_id = request.form.get('job')
    shift = request.form.get('shift')
    fte = request.form.get('fte')
    weekend_off = request.form.get('weekend_off')
    week_1_day_off = request.form.get('week_1_days_off')
    week_2_day_off = request.form.get('week_2_days_off')
    uniq_id = first+' '+last
    t_count = Employee.query.filter(
        Employee.uniq_id.like(f'{uniq_id}%')).count()
    if t_count > 0:
        uniq_id = uniq_id+f' {t_count+1}'
    if float(fte) < 40.0:
        emp_type = 'Part'
    else:
        emp_type = 'Full'
    # print(
    #     f"Job_id: {job_id}\nweek_1_day_off: {week_1_day_off}\nweek_2_day_off: {week_2_day_off}")
    if request.form.get('del_ind'):
        del_ind = 'Y'
    else:
        del_ind = 'N'
    if request.form.get('update') == None:
        emp_add = Employee(uniq_id=uniq_id, dept_id=dept_id,
                           emp_id=e_num, first_name=first, last_name=last,
                           job_id=job_id, emp_type=emp_type, shift=shift, weekend_off=weekend_off,
                           week_1_day_off=week_1_day_off, week_2_day_off=week_2_day_off,
                           fte=fte, create_time=datetime.now(),
                           modify_time=datetime.now(), create_by='Admin',
                           modify_by='Admin', del_ind=del_ind)
        db.session.add(emp_add)
        result = 'success'
    else:
        uniq_id = request.form.get('uniq_id')
        emp_update = Employee.query.get(uniq_id)
        emp_update.dept_id = dept_id
        emp_update.emp_id = e_num
        emp_update.first_name = first
        emp_update.last_name = last
        emp_update.job_id = job_id
        emp_update.week_1_day_off = week_1_day_off
        emp_update.week_2_day_off = week_2_day_off
        emp_update.emp_type = emp_type
        emp_update.shift = shift
        emp_update.weekend_off = weekend_off
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
    date = datetime.now()
    return render_template('Vacation.html', employee=emp, date=date.strftime('%m/%d/%Y'))


@app.route('/employee/vacationsubmit', methods=['GET', 'POST'])
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
    dept = Department.query.all()
    job = Job.query.order_by(Job.job_name).all()
    vac = Vacation.query.get(vac_id)
    dt = vac.employee
    db.session.delete(vac)
    db.session.commit()
    vac = dt.vacation
    if dt.del_ind.lower() == 'n':
        del_ind = None
    else:
        del_ind = 'checked=checked'
    return render_template("EmployeePage.html", dept=dept, submit='hidden',
                           update=None, dt=dt, del_ind=del_ind, vac=vac, job=job)


@app.route('/ScheduleSetting')
def schedule_setting():
    sch_all = ScheduleSetting.query.order_by(ScheduleSetting.job_name).all()
    job_opt = Job.query.order_by(Job.job_name).all()
    return render_template('ScheduleSetting.html', job=job_opt, sch_all=sch_all)


@app.route('/ScheduleSetting/Submit', methods=['GET', 'POST'])
def schedule_setting_submit():
    job = request.form.get('job')
    shift_start = request.form.get('shift_start')
    no_of_emp = request.form.get('no_of_emp')
    hr_per_shift = request.form.get('hr_per_shift')
    sun = request.form.get('sun')
    mon = request.form.get('mon')
    tue = request.form.get('tue')
    wed = request.form.get('wed')
    thur = request.form.get('thur')
    fri = request.form.get('fri')
    sat = request.form.get('sat')

    ct = ScheduleSetting.query.filter_by(job_id=job).count()+1
    job_name = f'{Job.query.get(job).job_name} {ct}'
    #print(f'Job name: {job_name} added')
    sch = ScheduleSetting(job_id=job, job_name=job_name, shift_start=shift_start,
                          no_of_emp=no_of_emp, hr_per_shift=hr_per_shift,
                          sun1=sun, mon1=mon, tue1=tue, wed1=wed, thur1=thur,
                          fri1=fri, sat1=sat, sun2=sun, mon2=mon, tue2=tue, wed2=wed,
                          thur2=thur, fri2=fri, sat2=sat)
    db.session.add(sch)
    db.session.commit()
    sch_all = ScheduleSetting.query.order_by(ScheduleSetting.job_name).all()
    job_opt = Job.query.order_by(Job.job_name).all()
    return render_template('ScheduleSetting.html', job=job_opt, sch_all=sch_all)


@app.route('/ScheduleSetting/Del/<sch_id>')
def schedule_setting_del(sch_id):
    sch = ScheduleSetting.query.get(sch_id)
    db.session.delete(sch)
    db.session.commit()

    sch_all = ScheduleSetting.query.order_by(ScheduleSetting.job_name).all()
    job_opt = Job.query.order_by(Job.job_name).all()
    return render_template('ScheduleSetting.html', job=job_opt, sch_all=sch_all)


@app.route('/_schedule_gen')
def _schedule_gen() -> str:
    """To change the employee  who has been scheduled in the Kitchen_schedule table.
    """
    global SQL_OPERATORS
    emp_id = request.args.get('emp_id', 0, type=str)
    emp_id = emp_id.replace('-', ' ')
    kitchen_id = request.args.get('kitchen_id', 0, type=str)
    col = request.args.get('col', 0, type=str)
    old_emp_id = request.args.get('old_emp_id', 0, type=str)
    chk1 = len(SQL_OPERATORS.findall(emp_id)) > 0 or len(
        SQL_OPERATORS.findall(kitchen_id)) > 0
    chk2 = len(SQL_OPERATORS.findall(col)) > 0 or len(
        SQL_OPERATORS.findall(old_emp_id)) > 0
    if chk1 or chk2:
        print('SQL Injection')
        return jsonify(result='SQL Injection')
    print(f"""----------------------------
    emp_id: {emp_id}
    kitchen_id: {kitchen_id}
    col: {col}
    old_emp_id: {old_emp_id}
----------------------""")
    kit_emp = Kitchen_schedule.query.get(kitchen_id)
    setattr(kit_emp, col, emp_id)
    db.session.commit()
    return jsonify(result='Sucess')


@app.route('/FnN/Downloads/<file>')
def FnN_downloads(file):
    if file == '1':
        table = pd.read_sql_table('kitchen_schedule', db.engine)
        table.drop(['kitchen_id', 'job_id', 'job_sub_id', 'time', 'job_group'], axis=1,
                   inplace=True)
        file_name = 'Schedule.csv'
    elif file == '2':
        table = pd.read_sql_table('emp_schedule', db.engine)
        table.drop(['people_id', 'emp_id', 'job_group'], axis=1,
                   inplace=True)
        file_name = 'EmployeeSchedule.csv'
    try:
        csv = table.to_csv(index=False)
    except:
        file_name = 'Invalid.csv'
        csv = "Error, contact admin"
    return Response(csv, mimetype='text/csv',
                    headers={"Content-disposition":
                             f"attachment; filename={file_name}"})

# -------NHSN App Starts here--------------


locations = {'BGH': ['ED', 'GICU', 'KM3', 'KM4', 'KM5', 'M3', 'M4', 'M5', 'M6', 'TCU'], 'CMH': ['ED', '3 West', '3S', '2 North', '2 South', '2 West', 'SCU'],
             'DVH': ['Addiction Rehab', 'Med Surg'],
             'WMH': ['CVICU', 'ED WIL', 'EXU', 'ICU', 'NSS', 'NB1', 'NICU', 'NT2',
                     'NT3', 'NT4', 'NT5', 'NW3', 'NW4', 'ST3', 'ST4', 'ST5', 'SSU']
             }


@app.route('/NHSN/ManualDataEntry', methods=['GET', 'POST'])
@app.route('/NHSN/ManualDataEntry/<campus>', methods=['GET', 'POST'])
def NHSN_DataEntryManual(campus=None):
    try:
        location = locations[campus]
    except:
        location = None
    return render_template('NHSNdataEntry.html', entry_type='Manual', locations=location,
                           url_fn='CentralLine_WMH', campus=campus)


@app.route('/NHSN/EPICDataEntry', methods=['GET', 'POST'])
@app.route('/NHSN/EPICDataEntry/<campus>', methods=['GET', 'POST'])
def NHSN_DataEntryEPIC(campus=None):
    try:
        location = locations[campus]
    except:
        location = None
    dates = [i[0] for i in NHSNdataEntry.query.with_entities(NHSNdataEntry.date.distinct()).order_by(
        NHSNdataEntry.date.desc()).all()]
    return render_template('NHSNdataEntry.html', entry_type='EPIC', locations=location,
                           url_fn='CentralLine_WMH', campus=campus, dates=dates)


@app.route('/NHSN/DataSubmit', methods=['GET', 'POST'])
def NHSN_DataSubmit():
    data = request.get_json()
    print(f'From IP::{request.remote_addr}: {data}')
    try:
        # if date is not present, then it program needs to goto except
        if pd.isna(pd.to_datetime(data['date'])):
            pd.NaT*timedelta(days=1)
        date = pd.to_datetime(data['date'])
        print(f'Try: {data["date"]}')
    except:
        date = datetime.now()
        if 17 < date.hour < 18 and data['entry_type'] == 'Manual':
            message = {'status': 'Failed',
                       'message': 'Data Entry not between 6 pm and 11 am.'}
            return jsonify(message)
        elif date.hour < 18:
            date = date - timedelta(days=1)
    nhsn_item_id = str(date.date())+data['campus']+data['unit']+data['measure']
    if data['entry_type'] == 'Manual':
        try:
            row = NHSNdataEntry.query.get(nhsn_item_id)
            row.manual_count = int(data['value'])
            print(f'M Count: {row.manual_count}\nE count: {row.epic_count}')
            if row.manual_count is not None and row.epic_count is not None:
                row.difference = abs(row.manual_count - row.epic_count)
                if row.manual_count == 0 and row.epic_count == 0:
                    row.difference_percent = 0
                elif row.manual_count == 0 or row.epic_count == 0:
                    row.difference_percent = 100
                else:
                    row.difference_percent = row.difference * 100 / row.manual_count
                    row.difference_percent = round(row.difference_percent, 2)
            row.modify_timestamp = datetime.now()
            row.modified_by = request.remote_addr
            #print('update manual')
        except:
            row = NHSNdataEntry(nhsn_item_id=nhsn_item_id, date=date.date(),
                                campus=data['campus'], unit=data['unit'], measure=data['measure'],
                                manual_count=int(data['value']), create_timestamp=datetime.now(),
                                create_by=request.remote_addr, modify_timestamp=datetime.now(),
                                modified_by=request.remote_addr)
            db.session.add(row)
    elif data['entry_type'] == 'EPIC':
        try:
            row = NHSNdataEntry.query.get(nhsn_item_id)
            row.epic_count = int(data['value'])
            if row.manual_count is not None and row.epic_count is not None:
                row.difference = abs(row.manual_count - row.epic_count)
                if row.manual_count == 0 and row.epic_count == 0:
                    row.difference_percent = 0
                elif row.manual_count == 0 or row.epic_count == 0:
                    row.difference_percent = 100
                else:
                    row.difference_percent = row.difference * 100 / row.manual_count
                    row.difference_percent = round(row.difference_percent, 2)
            # row.modify_timestamp = datetime.now()
            # row.modifieds_by = request.remote_addr

        except:
            row = NHSNdataEntry(nhsn_item_id=nhsn_item_id, date=date.date(),
                                campus=data['campus'], unit=data['unit'], measure=data['measure'],
                                epic_count=int(data['value']), create_timestamp=datetime.now(),
                                create_by=request.remote_addr, modify_timestamp=datetime.now(),
                                modified_by=request.remote_addr)
            db.session.add(row)
    db.session.commit()
    message = {'status': 'recieved', 'message': f'{datetime.now()}'}
    # message = {'status': 'Failed',
    #            'message': 'Data Entry not between 6 pm and 11 am.'}
    response = jsonify(message)
    return response


@app.route('/NHSN/Audit', methods=['GET', 'POST'])
@app.route('/NHSN/Audit/<campus>', methods=['GET', 'POST'])
def NHSN_Audit(campus='All'):
    date = request.form.get('date')
    # print(date)
    if campus == 'All':
        dates = [i[0] for i in NHSNdataEntry.query.with_entities(NHSNdataEntry.date.distinct()).order_by(
            NHSNdataEntry.date.desc()).all()]
        data = NHSNdataEntry.query.filter(NHSNdataEntry.date.in_([date]) if date is not None else
                                          NHSNdataEntry.date.in_(dates)).order_by(
            NHSNdataEntry.date.desc(), NHSNdataEntry.campus,
            NHSNdataEntry.measure, NHSNdataEntry.unit).all()

    else:
        dates = [i[0] for i in NHSNdataEntry.query.filter(NHSNdataEntry.campus == campus).with_entities(
            NHSNdataEntry.date.distinct()).order_by(NHSNdataEntry.date.desc()).all()]
        data = NHSNdataEntry.query.filter(and_(
            NHSNdataEntry.campus == campus, NHSNdataEntry.date.in_([date]) if date is not None else
            NHSNdataEntry.date.in_(dates))).order_by(
            NHSNdataEntry.date.desc(), NHSNdataEntry.campus,
            NHSNdataEntry.measure, NHSNdataEntry.unit).all()

    # print(max(NHSNdataEntry.date))
    return render_template('NHSN_Audit.html', data=data, campus=campus, dates=dates)


@app.route('/NHSN/Audit/UpdateData', methods=['GET', 'POST'])
def NHSN_DataUpdate():
    data = request.get_json()
    print(data)
    nhsn_item_id = data['nhsn_item_id']
    if data['entry_type'] == 'Manual':
        row = NHSNdataEntry.query.get(nhsn_item_id)
        row.audit = f"{datetime.now()} Manual Changed from {row.manual_count} to {data['value']}. {data['reason_for_change']}" if row.audit is None else row.audit + \
            f"\n{datetime.now()} Manual Changed from {row.manual_count} to {data['value']}. {data['reason_for_change']}"
        row.manual_count = int(data['value'])
        if row.manual_count is not None and row.epic_count is not None:
            row.difference = abs(row.manual_count - row.epic_count)
            if row.manual_count == 0 and row.epic_count == 0:
                row.difference_percent = 0
            elif row.manual_count == 0 or row.epic_count == 0:
                row.difference_percent = 100
            else:
                row.difference_percent = row.difference * 100 / row.manual_count
                row.difference_percent = round(row.difference_percent, 2)
        row.modify_timestamp = datetime.now()
        row.modified_by = request.remote_addr
        row.reason_for_change = data['reason_for_change']

    else:
        row = NHSNdataEntry.query.get(nhsn_item_id)
        row.audit = f"{datetime.now()} EPIC Changed from {row.epic_count} to {data['value']}. {data['reason_for_change']}" if row.audit is None else row.audit + \
            f"{datetime.now()} EPIC Changed from {row.epic_count} to {data['value']}. {data['reason_for_change']}"
        row.epic_count = int(data['value'])
        if row.manual_count is not None and row.epic_count is not None:
            row.difference = abs(row.manual_count - row.epic_count)
            if row.manual_count == 0 and row.epic_count == 0:
                row.difference_percent = 0
            elif row.manual_count == 0 or row.epic_count == 0:
                row.difference_percent = 100
            else:
                row.difference_percent = row.difference * 100 / row.manual_count
                row.difference_percent = round(row.difference_percent, 2)
        row.modify_timestamp = datetime.now()
        row.modified_by = request.remote_addr
        row.reason_for_change = data['reason_for_change']
    db.session.commit()
    message = {'status': 'updated', 'message': f'{datetime.now()}'}
    # message = {'status': 'Failed',
    #            'message': 'Data Entry not between 6 pm and 11 am.'}
    response = jsonify(message)
    return response


@app.route('/test', methods=['GET', 'POST'])
def test():

    if request.method == 'POST':
        import operation
        operation.main()
    emp_dtl = request.form.get('emp_dtl')
    if emp_dtl != None:
        #print('EmpSearch if stmt..')
        emp_dtl_f = func.lower(f'%{emp_dtl}%')
        emp_list = Kitchen_schedule.query.filter(or_(
            func.lower(Kitchen_schedule.Job).like(emp_dtl_f),
            func.lower(Kitchen_schedule.Sun1).like(emp_dtl_f),
            func.lower(Kitchen_schedule.Mon1).like(emp_dtl_f))
        ).order_by(Kitchen_schedule.kitchen_id)

    else:
        #print('EmpSearch else stmt..')
        emp_list = Kitchen_schedule.query.order_by(
            Kitchen_schedule.kitchen_id).all()
    emp = Employee.query.order_by(Employee.uniq_id).all()
    return render_template('test.html', items=emp_list, emp=emp)


# -------OccMed App Starts here--------------


@app.route('/OccMed/CheckIn', methods=['GET', 'POST'])
def checkIn():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        campus = request.form.get('campus')
        dept = request.form.get('dept')
        reason = request.form.get('reason')
        comments = request.form.get('comments')

        occ = OccMedCheckIn(first_name=first_name, last_name=last_name,
                            campus=campus, dept=dept, reason=reason,
                            comments=comments, checkin_time=datetime.now())
        db.session.add(occ)
        db.session.commit()
    checkInTable = OccMedCheckIn.query.all()
    return render_template('OccMedCheckIn.html', checkInTable=checkInTable)


if __name__ == "__main__":
    app.run()
