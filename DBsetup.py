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
    del_ind text,
    foreign key(dept_id) REFERENCES department(dept_id)
    )
    """)
conn.commit()

c.execute("insert into employee values ('10', 1, '0', 'Beeth', 'Bef', 'cook', 'AM', 'Sunday', 40.0, '5/23/20 23:14', '5/23/20 23:14', 'Admin', 'Admin', 'n');")
c.execute("insert into employee values ('11', 1, '1', 'Beeth', 'Acs', 'Ba', 'PM', 'Tuesday', 40.0, '5/23/20 23:14', '5/23/20 23:14', 'Admin', 'Admin', 'n');")
c.execute("insert into employee values ('12', 1, '2', 'Zen', 'Ae4b', 'Cook', 'AM/PM', 'Monday', 32.0, '5/23/20 23:18', '5/23/20 23:18', 'Admin', 'Admin', 'n');")
c.execute("insert into employee values ('13', 1, '3', 'Zen', 'Ben', 'cook', 'AM', 'Sunday', 24.0, '5/22/20 19:50', '5/22/20 19:50', 'Admin', 'Admin', 'n');")
c.execute("insert into employee values ('14', 1, '4', 'Beeth', 'Blam', 'Bill', 'AM', 'Tuesday', 20.0, '5/22/20 19:50', '5/22/20 19:50', 'Admin', 'Admin', 'n');")
c.execute("insert into employee values ('15', 1, '5', 'Zlaten', 'Zener', 'Bus', 'PM', 'Thursday', 40.0, '5/22/20 19:51', '5/22/20 19:51', 'Admin', 'Admin', 'n');")
c.execute("insert into employee values ('16', 1, '6', 'Chopin', 'SDF', 'Cr', 'AM/PM', 'Tuesday', 40.0, '5/22/20 19:57', '5/22/20 19:57', 'Admin', 'Admin', 'n');")
c.execute("insert into employee values ('17', 1, '7', 'Gomma', 'Bleo', 'Tend', 'AM', 'Thursday', 32.0, '5/22/20 19:58', '5/22/20 19:58', 'Admin', 'Admin', 'n');")
c.execute("insert into employee values ('18', 1, '8', 'Solam', 'Bleo', 'Tend', 'AM', 'Thursday', 24.0, '5/22/20 0:00', '5/22/20 0:00', 'Admin', 'Admin', 'n');")
c.execute("insert into employee values ('19', 1, '9', 'Gomma', 'Gomez', 'Carlos', 'AM', 'Thursday', 20.0, '5/21/20 0:00', '5/21/20 0:00', 'Admin', 'Admin', 'n');")
c.execute("insert into employee values ('110', 1, '10', 'Zen', 'Ae4b', 'Cook', 'AM/PM', 'Monday', 40.0, '5/26/20 22:26', '5/26/20 22:26', 'Admin', 'Admin', 'n');")
c.execute("insert into employee values ('111', 1, '11', 'Chopin', 'Ben', 'Cook', 'AM', 'Monday', 40.0, '5/26/20 22:32', '5/26/20 22:32', 'Admin', 'Admin', 'n');")

conn.commit()

conn.close()