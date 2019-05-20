import hashlib
from flask import Flask
from models.model import db
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
from flask import make_response

from logic.API import API
from logic.Auth import Auth
from logic.Db import Db
from logic.PrepareRequest import PrepareRequest
from logic.PrepareResponse import PrepareResponse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.db3'

db.init_app(app)
auth = Auth()
dbWorker = Db()

@app.route('/createall')
def createAll():
    db.create_all()
    return redirect(url_for('index'))


@app.route('/')
def index():
    if not auth.isLoggedUser(request.cookies):
        return redirect(url_for('login'))

    return render_template('index.html')


@app.route('/place')
def place():
    return render_template('place.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth.html')

    elif request.method == 'POST':
        if auth.login(request.form.get('login'), request.form.get('password')):
            resp = make_response(redirect(url_for('index')))
            h = hashlib.sha1(str.encode(request.form.get('password')))
            p = h.hexdigest()
            resp.set_cookie('userID', p)
            resp.set_cookie('userLogin', request.form.get('login'))
            return resp
        else:
            return render_template('auth.html', errors=['Не верный логин или пароль'])


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    
    elif request.method == 'POST':
        password = request.form.get('password')
        secondPassword = request.form.get('password_confirm')
        if auth.validate(request.form):
            print('hello')
            dbWorker.addUser(request.form.get('login'), request.form.get('password'))
            print('world')
            return redirect(url_for('login'))
        else:
            return render_template('registration.html', errors=['Данные введены не верно'])
        

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('userID', '', expires=0)
    resp.set_cookie('userLogin', '', expires=0)
    return resp