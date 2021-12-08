from application import app
from flask import render_template

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", login=False)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/manage')
def manage():
    return render_template("manage.html")