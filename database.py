import sqlite3
conn=sqlite3.connect('./instances/YWS.db')
cursor=conn.cursor()


cursor.execute('''
''')


conn.commit()
cursor.close()
conn.close()

# TODO
# 1. Change the column o_date to to_date

# CREATE TABLE users (
#     uid INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     lastname TEXT NOT NULL,
#     phone_no TEXT NOT NULL,
#     password TEXT NOT NULL
# )

# CREATE TABLE courses (
#     cid INTEGER PRIMARY KEY AUTOINCREMENT,
#     course_name TEXT NOT NULL,
#     price REAL NOT NULL,
#     from_date DATE NOT NULL,
#     o_date DATE NOT NULL
# )

# CREATE TABLE enrollments (
#     uid INTEGER NOT NULL,
#     cid INTEGER NOT NULL,
#     fee REAL NOT NULL,
#     enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY (uid, cid),
#     FOREIGN KEY (uid) REFERENCES users(uid),
#     FOREIGN KEY (cid) REFERENCES courses(cid)
# )

# CREATE TRIGGER IF NOT EXISTS set_fee_on_enrollment
# AFTER INSERT ON enrollments
# FOR EACH ROW
# BEGIN
#     UPDATE enrollments
#     SET fee = (SELECT price FROM courses WHERE cid = NEW.cid)
#     WHERE rowid = NEW.rowid;
# END;

# INSERT INTO enrollments (uid, cid, fee)
# VALUES (1, 1, 199.99)


