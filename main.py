from flask import Flask, render_template, request, redirect, url_for, flash, g, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flashing messages

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('./instances/YWS.db')
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['secondName']
        phone_no = request.form['phoneNo']
        gender = request.form['Gender']
        password = generate_password_hash(request.form['password'])

        db = get_db()
        cursor = db.cursor()

        # Check if the phone number already exists
        cursor.execute('SELECT Ph_no FROM users WHERE Ph_no = ?', (phone_no,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Phone number already registered. Please use a different phone number.", "error")
            return redirect(url_for('success'))  # Redirect back to the registration page

        # If phone number doesn't exist, insert the new user
        cursor.execute('''
            INSERT INTO users (name, lastname, Ph_no, gender, password)
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, phone_no, gender, password))
        db.commit()

        flash("Registration successful!", "success")
        return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phoneNo']
        password = request.form['password']

        # Special admin login
        if phone == '9999999999' and password == 'yogaws':
            session['user_type'] = 'admin'
            return redirect(url_for('admin'))

        # Connect to the database
        db = get_db()
        cursor = db.cursor()

        # Check users table
        cursor.execute('SELECT * FROM users WHERE Ph_no = ?', (phone,))
        user = cursor.fetchone()

        if user and check_password_hash(user[5], password):  
            session['user_type'] = 'user'
            session['user_id'] = user[0]  
            return redirect(url_for('success'))

        # Check instructors table
        cursor.execute('SELECT * FROM instructors WHERE Ph_no = ?', (phone,))
        instructor = cursor.fetchone()

        if instructor:
            stored_password = instructor[8]  
            if check_password_hash(stored_password, password):
                # If user is found in 'instructors' table
                session['user_type'] = 'instructor'
                session['instructor_id'] = instructor[0]  
                return redirect(url_for('dashboard'))

        # If no matching user is found
        flash("Invalid phone number or password", "danger")
        return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['lname']
        dob_day = request.form['dob-date']
        dob_month = request.form['dob-month']
        dob_year = request.form['dob-year']
        address = request.form['address']
        address2 = request.form['address2']
        city = request.form['city']
        state = request.form['state']
        postal = request.form['postal']
        phone = request.form['phone']
        position = request.form['position']
        hear = request.form['hear']
        password = request.form['password']  

        # Format the date of birth
        dob = f"{dob_year}-{dob_month}-{dob_day}"

        # Connect to the database
        db = get_db()
        cursor = db.cursor()

        # Check if the phone number already exists
        cursor.execute('SELECT * FROM instructors WHERE Ph_no = ?', (phone,))
        existing_instructor = cursor.fetchone()

        if existing_instructor:
            flash("Phone number already registered. Please use a different number.", "error")
            return redirect(url_for('apply'))  # Redirect back to the application form

        # Insert data into the instructors table
        cursor.execute('''
            INSERT INTO instructors (name, lastname, Ph_no, DOB, Address, Course, reference, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, phone, dob, f"{address}, {address2}, {city}, {state}, {postal}", position, hear, generate_password_hash(password)))
        
        db.commit()
        
        flash("Application submitted successfully!", "success")
        return redirect(url_for('success'))  # Redirect to a success page

    return render_template('appl.html')


@app.route('/dashboard')
def dashboard():
    return render_template('teach.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('index'))


@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/vision', methods=['GET'])
def vision():
    return render_template('visionNmission.html')


@app.route('/admin')
def admin():
    db = get_db()
    cursor = db.cursor()

    # Total enrollments (entries in applicants table)
    cursor.execute('SELECT COUNT(*) FROM applicants')
    total_enrollments = cursor.fetchone()[0]

    # Total instructors (entries in instructors table)
    cursor.execute('SELECT COUNT(*) FROM instructors')
    total_instructors = cursor.fetchone()[0]

    # Total courses (entries in course table)
    cursor.execute('SELECT COUNT(*) FROM course')
    total_courses = cursor.fetchone()[0]

    # Total income (sum of Fees in applicants table)
    cursor.execute('SELECT SUM(Fees) FROM applicants')
    total_income = cursor.fetchone()[0] or 0  # Default to 0 if there are no fees

    # New students (first 10 entries from applicants table, join with users to get names)
    cursor.execute('''
        SELECT u.name, u.lastname 
        FROM applicants a 
        JOIN users u ON a.UID = u.UID 
        LIMIT 10
    ''')
    new_students = cursor.fetchall()

    return render_template(
        'admin.html',
        total_enrollments=total_enrollments,
        total_instructors=total_instructors,
        total_courses=total_courses,
        total_income=total_income,
        new_students=new_students
)

@app.route('/view_all_students')
def view_all_students():
    # Connect to the database
    conn = sqlite3.connect('./instances/YWS.db')
    cursor = conn.cursor()

    # Query to get the students' first name, last name, and course name from the applicants table
    cursor.execute('''
        SELECT users.name, users.lastname, course.Course_name 
        FROM applicants 
        JOIN users ON applicants.UID = users.UID
        JOIN course ON applicants.CID = course.CID
    ''')
    students = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    # Pass the data to the template
    return render_template('view_all_students.html', students=students)


if __name__ == '__main__':
    app.run(debug=True)
