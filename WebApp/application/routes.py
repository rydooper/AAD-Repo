from application import app
import secrets
from flask import Flask, get_flashed_messages, render_template, redirect, send_from_directory, url_for, request, session, flash
from werkzeug.utils import secure_filename
import sys, os

ALLOWED_EXTENSIONS = {'txt', 'csv'}

sys.path.insert(1, '../DesktopApp/')
from fridge_db import login as dbLogin


app.secret_key = secrets.token_hex()

#from flask docs
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        #replace this
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session["username"] = request.form['username']
            return redirect(url_for('manage'))
    return render_template('login.html', error=error)

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if "username" not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash ('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            #secure filename prevents filename uploads that could compromise server
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("File successfully uploaded")
    return render_template("manage.html")