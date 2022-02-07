from flask import Flask

app = Flask(__name__)

from application import routes

UPLOAD_FOLDER = './uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER