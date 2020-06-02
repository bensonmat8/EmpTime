import sqlite3

conn = sqlite3.connect('employee.db')
c = conn.cursor()
c.execute("""create table department(
    dept_id integer primary key,
    dept_name text)""")
c.execute("insert into department(dept_name) values ('Food and Nutrition')")

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
    foreign key(dept_id) REFERENCES department(dept_id)
    )
    """)
conn.commit()

c.execute("insert into employee values ('10', 1, '0', 'Beeth', 'Bef', 'cook', 'AM', 'Sunday', 40.0, '5/23/20 11:14 PM', '5/23/20 11:14 PM', 'Admin', 'Admin');")
c.execute("insert into employee values ('11', 1, '1', 'Beeth', 'Acs', 'Ba', 'PM', 'Tuesday', 40.0, '5/23/20 11:14 PM', '5/23/20 11:14 PM', 'Admin', 'Admin');")
c.execute("insert into employee values ('12', 1, '2', 'Zen', 'Ae4b', 'Cook', 'AM/PM', 'Monday', 32.0, '5/23/20 11:18 PM', '5/23/20 11:18 PM', 'Admin', 'Admin');")
c.execute("insert into employee values ('13', 1, '3', 'Zen', 'Ben', 'cook', 'AM', 'Sunday', 24.0, '5/22/20 7:50 PM', '5/22/20 7:50 PM', 'Admin', 'Admin');")
c.execute("insert into employee values ('14', 1, '4', 'Beeth', 'Blam', 'Bill', 'AM', 'Tuesday', 20.0, '5/22/20 7:50 PM', '5/22/20 7:50 PM', 'Admin', 'Admin');")
c.execute("insert into employee values ('15', 1, '5', 'Zlaten', 'Zener', 'Bus', 'PM', 'Thursday', 40.0, '5/22/20 7:51 PM', '5/22/20 7:51 PM', 'Admin', 'Admin');")
c.execute("insert into employee values ('16', 1, '6', 'Chopin', 'SDF', 'Cr', 'AM/PM', 'Tuesday', 40.0, '5/22/20 7:57 PM', '5/22/20 7:57 PM', 'Admin', 'Admin');")
c.execute("insert into employee values ('17', 1, '7', 'Gomma', 'Bleo', 'Tend', 'AM', 'Thursday', 32.0, '5/22/20 7:58 PM', '5/22/20 7:58 PM', 'Admin', 'Admin');")
c.execute("insert into employee values ('18', 1, '8', 'Smith', 'Blag', 'Tend', 'AM', 'Thursday', 24.0, '5/22/20 12:00 AM', '5/22/20 12:00 AM', 'Admin', 'Admin');")
c.execute("insert into employee values ('19', 1, '9', 'Jomma', 'Gomez', 'Carlos', 'AM', 'Thursday', 20.0, '5/21/20 12:00 AM', '5/21/20 12:00 AM', 'Admin', 'Admin');")
c.execute("insert into employee values ('110', 1, '10', 'Zen', 'Ae4b', 'Cook', 'AM/PM', 'Monday', 40.0, '5/26/20 10:26 PM', '5/26/20 10:26 PM', 'Admin', 'Admin');")
c.execute("insert into employee values ('111', 1, '11', 'Chopin', 'Ben', 'Cook', 'AM', 'Monday', 40.0, '5/26/20 10:32 PM', '5/26/20 10:32 PM', 'Admin', 'Admin');")


conn.commit()

conn.close()