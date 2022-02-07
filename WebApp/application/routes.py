from application import app
import secrets
from flask import Flask, render_template, redirect, url_for, request, session
import sys

sys.path.insert(1, '../DesktopApp/')
from fridge_db import login as dbLogin

app.secret_key = secrets.token_hex()

@app.route('/')
@app.route('/home')
def home():
    if 'username' not in session:
        return render_template("home.html", login=False)
    return render_template("home.html", login=True)

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for('home'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        print(dbLogin(request.form['username'], request.form['password']))
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session["username"] = request.form['username']
            return redirect(url_for('manage'))
    return render_template('login.html', error=error)

@app.route('/manage')
def manage():
    if "username" not in session:
        return redirect(url_for('login'))
    return render_template("manage.html")