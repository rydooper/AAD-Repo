from application import app
import secrets
from flask import Flask, get_flashed_messages, render_template, redirect, send_from_directory, url_for, request, session, flash
from werkzeug.utils import secure_filename
import sys, os
from csv import reader

ALLOWED_EXTENSIONS = {'txt', 'csv'}

sys.path.insert(1, '../DesktopApp/')
from fridge_db import login as dbLogin, signup as dbSignup, add_items, authenticate_code

app.secret_key = secrets.token_hex()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_db(filename):
    with open (f'./uploads/{filename}') as f:
        csv_reader = reader(f)
        for row in csv_reader:
            test = add_items(row[0], row[1], row[2], row[3], row[4], row[5])
    
    if test == "Successful query.":
        flash("...and added to database!")
    elif test == "Unsuccessful query.":
        flash("...but failed to add to database. Please try again.")
    print(test)



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
        loginResponse = dbLogin(request.form['username'], request.form['password'])
        type(loginResponse)
        if type(loginResponse) == str:
            # unsuccessful login
            error = loginResponse
            return render_template('login.html', error=error)
        else:
            session["username"] = request.form['username']
            return redirect(url_for('manage'))
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        signupResponse = dbSignup(request.form['username'], request.form['password'], request.form['name'], 'Delivery Driver', 'NULL')
        return redirect(url_for('login'))

    return render_template('signup.html', error=error)

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if "username" not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        doorcode = request.form['doorcode']
        if not authenticate_code(doorcode):
            flash('Incorrect door code.')
            return redirect(request.url)

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash ('No selected file')
            return redirect(request.url)
        
        if file and not allowed_file(file.filename):
            flash("Invalid file type")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            #secure filename prevents filename uploads that could compromise server
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("File successfully uploaded...")
            upload_to_db(filename)
    return render_template("manage.html")