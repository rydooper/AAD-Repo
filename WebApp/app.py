from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/cunt')
def cunt():
    return 'Hello, cunt!'