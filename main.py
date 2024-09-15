from flask import Flask, render_template, request, redirect, url_for, flash, g, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

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
            return redirect(url_for('gallery'))  # Redirect back to the application form

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

@app.route('/vision')
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

#all about enrollment display and delete    
@app.route('/edit_enrollments')
def edit_enrollments():
    # Connect to the database
    db = get_db()
    cursor = db.cursor()

    # Query to get the user's name, lastname, course name, and fees paid
    cursor.execute('''
        SELECT users.name, users.lastname, applicants.Course_name, applicants.Fees, applicants.APPID
        FROM applicants 
        JOIN users ON applicants.UID = users.UID
    ''')
    enrollments = cursor.fetchall()

    # Close the connection
    cursor.close()

    # Render enrollments.html and pass the enrollments data
    return render_template('enrollments.html', enrollments=enrollments)

@app.route('/delete_enrollment/<int:appid>', methods=['POST'])
def delete_enrollment(appid):
    db = get_db()
    cursor = db.cursor()

    # First, fetch the UID of the user associated with the given APPID
    cursor.execute('SELECT UID FROM applicants WHERE APPID = ?', (appid,))
    user = cursor.fetchone()

    if user:
        uid = user[0]

        # Delete the enrollment from the applicants table
        cursor.execute('DELETE FROM applicants WHERE APPID = ?', (appid,))
        db.commit()

        # Now delete the user from the users table based on the UID
        cursor.execute('DELETE FROM users WHERE UID = ?', (uid,))
        db.commit()

        flash("Enrollment and user deleted successfully!", "success")
    else:
        flash("User not found or already deleted.", "error")

    return redirect(url_for('edit_enrollments'))

#all about editing instructors and deleting them
@app.route('/edit_instructors', methods=['GET', 'POST'])
def edit_instructors():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Handle adding a new instructor
        name = request.form['name']
        lastname = request.form['lastname']
        phone = request.form['phone']
        dob = request.form['dob']
        course_name = request.form['course']  # Save course name instead of course_id
        password = generate_password_hash(request.form['password'])
        reference = request.form.get('reference', '')

        # Get full address from form
        address = request.form['address']
        address2 = request.form.get('address2', '')
        city = request.form['city']
        state = request.form['state']
        postal = request.form['postal']

        full_address = f"{address}, {address2}, {city}, {state}, {postal}"

        # Insert new instructor data into the instructors table
        cursor.execute('''
            INSERT INTO instructors (name, lastname, Ph_no, DOB, Address, Course, reference, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, lastname, phone, dob, full_address, course_name, reference, password))
        db.commit()

        flash("Instructor added successfully!", "success")
        return redirect(url_for('edit_instructors'))

    # Query to display existing instructors
    cursor.execute('''
        SELECT i.name, i.lastname, i.Course, i.Ph_no, i.Address, i.TID 
        FROM instructors i
    ''')
    instructors = cursor.fetchall()

    # Fetch all courses for the dropdown in the add-instructor form
    cursor.execute('SELECT CID, Course_name FROM course')
    courses = cursor.fetchall()

    return render_template('instructors.html', instructors=instructors, courses=courses)


@app.route('/delete_instructor_enrollment/<int:tid>', methods=['POST'])
def delete_instructor_enrollment(tid):
    db = get_db()
    cursor = db.cursor()

    # Delete instructor from instructors table
    cursor.execute('DELETE FROM instructors WHERE TID = ?', (tid,))
    db.commit()

    flash("Instructor and their data deleted successfully!", "success")
    return redirect(url_for('edit_instructors'))


#all about editing course
@app.route('/edit_course', methods=['GET', 'POST'])
def edit_course():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Check if the request is for adding a new course or updating an existing course
        if 'course_id' in request.form:
            # Update existing course's start and end dates
            course_id = request.form['course_id']
            from_date = request.form['from_date']
            to_date = request.form['to_date']

            cursor.execute('''
                UPDATE course
                SET from_date = ?, to_date = ?
                WHERE CID = ?
            ''', (from_date, to_date, course_id))
            db.commit()
            flash("Course dates updated successfully!", "success")

        else:
            # Insert new course
            course_name = request.form['course_name']
            price = request.form['price']
            from_date = request.form['from_date']
            to_date = request.form['to_date']

            cursor.execute('''
                INSERT INTO course (Course_name, Price, from_date, to_date)
                VALUES (?, ?, ?, ?)
            ''', (course_name, price, from_date, to_date))
            db.commit()
            flash("Course added successfully!", "success")

        return redirect(url_for('edit_course'))

    # Fetch all courses when the method is GET
    cursor.execute('SELECT CID, Course_name, Price, from_date, to_date FROM course')
    courses = cursor.fetchall()

    return render_template('course.html', courses=courses)

@app.route('/delete_course/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    db = get_db()
    cursor = db.cursor()

    # Find and delete the course by course_id
    cursor.execute('DELETE FROM course WHERE CID = ?', (course_id,))
    db.commit()

    flash("Course deleted successfully!", "success")
    return redirect(url_for('edit_course'))





@app.route('/view_all_students')
def view_all_students():
    # Connect to the database
    conn = sqlite3.connect('./instances/YWS.db')
    cursor = conn.cursor()

    # Query to get the students' first name, last name, and course name from the applicants table
    # changed by parthk
    cursor.execute('''
        SELECT users.name, users.lastname, applicants.Course_name
        FROM applicants 
        JOIN users ON applicants.UID = users.UID
    ''')
    students = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()
    print(students)  # Check if this prints a non-empty list
    # Pass the data to the template
    return render_template('view_all_students.html', students=students)


if __name__ == '__main__':
    app.run(debug=True)
