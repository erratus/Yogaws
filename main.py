from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'TEST'  # Set a proper secret key for session management

def get_db_connection():
    conn = sqlite3.connect('./instances/YWS.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html', title='homepage')

@app.route('/templates/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user is None or not check_password_hash(user['password'], password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        session['user_id'] = user['id']
        session['username'] = user['username']
        return redirect(url_for('home'))

    return render_template('login.html', title='Login')


if __name__ == '__main__':
    app.run(debug=True)
