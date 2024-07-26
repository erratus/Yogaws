from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app=Flask(__name__)
# app.secret_key('TEST')
# conn=sqlite3.connect('./instances/YWS.db',check_same_thread=False)
# cursor=conn.cursor()
# app.app_context().push()

@app.route('/')
def home():
    return render_template('index.html', title='homepage')