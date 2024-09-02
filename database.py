import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('./instances/YWS.db')
cursor = conn.cursor()

# # Create the users table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS users (
#     UID INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT,
#     lastname TEXT,
#     Ph_no TEXT,
#     gender TEXT,
#     password TEXT
# );
# ''')

# # Create the instructors table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS instructors (
#     TID INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT,
#     lastname TEXT,
#     Ph_no TEXT,
#     DOB TEXT,
#     Address TEXT,
#     Course INTEGER,
#     reference TEXT,
#     password TEXT, 
#     FOREIGN KEY (Course) REFERENCES course(CID)
# );
# ''')

# # Create the course table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS course (
#     CID INTEGER PRIMARY KEY AUTOINCREMENT,
#     Course_name TEXT,
#     Price REAL,
#     to_date TEXT,
#     from_date TEXT
# );
# ''')

# # Create the applicants table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS applicants (
#     APPID INTEGER PRIMARY KEY AUTOINCREMENT,
#     UID INTEGER,
#     CID INTEGER,
#     Fees REAL,
#     Course_name TEXT,
#     FOREIGN KEY (UID) REFERENCES users(UID),
#     FOREIGN KEY (CID) REFERENCES course(CID)
# );
# ''')

# cursor.execute('''
# INSERT INTO applicants (UID, CID, Fees, Course_name)
# VALUES 
#     (1, 1, 500.00, 'Yoga Basics'),
#     (2, 2, 700.00, 'Advanced Yoga'),
#     (3, 1, 550.00, 'Yoga Basics'),
#     (4, 3, 800.00, 'Yoga for Flexibility'),
#     (5, 2, 750.00, 'Advanced Yoga');
# ''')


# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
