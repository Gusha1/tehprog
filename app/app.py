from flask import Flask
from models.model import db
from flask import redirect
from flask import url_for
from flask import render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.db3'

db.init_app(app)

@app.route('/')
def index():
	return render_template('index.html')
