import sqlite3

conn = sqlite3.connect('employee.db')
c = conn.cursor()
c.execute("""create table employee (
    e_num text,
    first text,
    last text,
    title text,
    shift text,
    days_off text,
    fte real,
    create_time datetime,
    modify_time datetime,
    create_by text,
    modify_by text
    )
    """)
conn.commit()
conn.close()