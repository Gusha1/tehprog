from flask import Flask
from models.model import db
from flask import redirect
from flask import url_for
from flask import render_template


from logic.API import API
from logic.Auth import Auth
from logic.Db import Db
from logic.PrepareRequest import PrepareRequest
from logic.PrepareResponse import PrepareResponse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.db3'

db.init_app(app)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/place')
def index():
	return render_template('place.html')