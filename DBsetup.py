import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


chk = input('Create local database? (y/n)')
if chk.lower=='y':
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    try:
        c.execute("""create table department(
            dept_id integer primary key,
            dept_name text)""")
        c.execute("insert into department(dept_name) values ('Food and Nutrition')")
    except:
        pass
    c.execute("""create table employee (
        uniq_id text primary key,
        dept_id integer,
        emp_id text,
        first_name text,
        last_name text,
        title text,
        shift text,
        days_off text,
        fte real,
        create_time datetime,
        modify_time datetime,
        create_by text,
        modify_by text,
        del_ind text,
        foreign key(dept_id) REFERENCES department(dept_id)
        )
        """)
    conn.commit()
    
else:
    import os
    engine2 = create_engine('postgresql:///bensonshajimathew')
    c  = scoped_session(sessionmaker(engine2))


c.execute("""insert into employee values
    ('10', 1, '0', 'Beeth', 'Bef', 'cook', 'AM', 'First Weekend', 40.0, '5/23/20 11:14 PM', '5/23/20 11:14 PM', 'Admin', 'Admin', 'n'),
 ('11', 1, '1', 'Beeth', 'Acs', 'Ba', 'PM', 'Second Weekend', 40.0, '5/23/20 11:14 PM', '5/23/20 11:14 PM', 'Admin', 'Admin', 'n'),
 ('12', 1, '2', 'Zen', 'Ae4b', 'Cook', 'AM/PM', 'Second Weekend', 32.0, '5/23/20 11:18 PM', '5/23/20 11:18 PM', 'Admin', 'Admin', 'n'),
 ('13', 1, '3', 'Zen', 'Ben', 'cook', 'AM', 'Second Weekend', 24.0, '5/22/20 7:50 PM', '5/22/20 7:50 PM', 'Admin', 'Admin', 'n'),
 ('14', 1, '4', 'Beeth', 'Blam', 'Bill', 'AM', 'First Weekend', 20.0, '5/22/20 7:50 PM', '5/22/20 7:50 PM', 'Admin', 'Admin', 'n'),
 ('15', 1, '5', 'Zlaten', 'Zener', 'Bus', 'PM', 'Second Weekend', 40.0, '5/22/20 7:51 PM', '5/22/20 7:51 PM', 'Admin', 'Admin', 'n'),
 ('16', 1, '6', 'Chopin', 'SDF', 'Cr', 'AM/PM', 'Second Weekend', 40.0, '5/22/20 7:57 PM', '5/22/20 7:57 PM', 'Admin', 'Admin', 'n'),
 ('17', 1, '7', 'Gomma', 'Bleo', 'Tend', 'AM', 'First Weekend', 32.0, '5/22/20 7:58 PM', '5/22/20 7:58 PM', 'Admin', 'Admin', 'n'),
 ('18', 1, '8', 'Solam', 'Bleo', 'Tend', 'AM', 'Second Weekend', 24.0, '5/22/20 12:00 AM', '5/22/20 12:00 AM', 'Admin', 'Admin', 'n'),
 ('19', 1, '9', 'Gomma', 'Gomez', 'Carlos', 'AM', 'Second Weekend', 20.0, '5/21/20 12:00 AM', '5/21/20 12:00 AM', 'Admin', 'Admin', 'n'),
 ('110', 1, '10', 'Zen', 'Ae4b', 'Cook', 'AM/PM', 'First Weekend', 40.0, '5/26/20 10:26 PM', '5/26/20 10:26 PM', 'Admin', 'Admin', 'n'),
 ('111', 1, '11', 'Ben', 'Chopin', 'Cook', 'AM', 'Second Weekend', 40.0, '5/26/20 10:32 PM', '6/10/20 10:04 PM', 'Admin', 'Admin', 'n'),
 ('1Q115', 1, 'Q115', 'Chopin', 'Ber', 'Cook', 'AM', 'First Weekend', 33.0, '6/3/20 10:32 PM', '6/3/20 10:32 PM', 'Admin', 'Admin', 'n'),
 ('1t', 1, 't', 'test', 'test', 'test', 'AM', 'Second Weekend', 33.0, '6/3/20 10:45 PM', '6/3/20 10:45 PM', 'Admin', 'Admin', 'n'),
 ('119', 1, '19', 'Gwen', 'Satt', 'Singer', 'PM', 'Second Weekend', 20.0, '6/3/20 11:20 PM', '6/3/20 11:20 PM', 'Admin', 'Admin', 'n'),
 ('1193', 1, '193', 'Gwen', 'Satt', 'Singer', 'PM', 'First Weekend', 20.0, '6/3/20 11:20 PM', '6/3/20 11:20 PM', 'Admin', 'Admin', 'n'),
 ('1EdBd2', 1, 'EdBd2', 'Bd', 'wef', 'df', 'PM', 'First Weekend', 22.0, '6/3/20 11:23 PM', '6/3/20 11:23 PM', 'Admin', 'Admin', 'n'),
 ('1E11523', 1, 'E11523', 'Gorsh', 'Will', 'Cook', 'AM', 'Second Weekend', 22.0, '6/8/20 11:05 PM', '6/8/20 11:05 PM', 'Admin', 'Admin', 'n'),
 ('1E11524', 1, 'E11524', 'DaWill', 'McGorsh', 'Cook', 'AM', 'Second Weekend', 32.0, '6/8/20 11:05 PM', '6/10/20 9:16 PM', 'Admin', 'Admin', 'n'),
 ('1E11525', 1, 'E11525', 'McGorsh', 'DaWill', 'Cook', 'AM', 'First Weekend', 32.0, '6/8/20 11:09 PM', '6/8/20 11:09 PM', 'Admin', 'Admin', 'n'),
 ('1E11526', 1, 'E11526', 'Chandi', 'Addu', 'Driver', 'AM', 'Second Weekend', 22.0, '6/8/20 11:15 PM', '6/8/20 11:15 PM', 'Admin', 'Admin', 'n'),
 ('1E1345', 1, 'E1345', 'Chenna', 'Ri', 'Cook', 'AM/PM', 'First Weekend', 60.0, '6/10/20 10:05 PM', '6/10/20 10:05 PM', 'Admin', 'Admin', 'n')"""
)
try:
    conn.commit()
    conn.close()
except:
    c.commit()
    c.close()

