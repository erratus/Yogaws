from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'TEST'  # Set a proper secret key for session management

def get_db_connection():
    conn = sqlite3.connect('./instances/YWS.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html', title='homepage')

# Add additional routes and logic as needed

if __name__ == '__main__':
    app.run(debug=True)
