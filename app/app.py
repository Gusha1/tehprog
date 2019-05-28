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

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.db3'

db.init_app(app)
auth = Auth()
dbWorker = Db()
prepareRequest = PrepareRequest()
api = API()

@app.route('/createall')
def createAll():
    db.create_all()
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        places = api.getPlaces(prepareRequest.prepareList({}))
        if not auth.isLoggedUser(request.cookies):
            return render_template('index.html', places=places, auth=False)

        user = dbWorker.getUser(request.cookies.get('userLogin'))
        sortedPlaces = []

        hidedPlaces = dbWorker.getHidedPlaces(user.id)
        for i in range(len(places)):
            flag = False
            for j in range(len(hidedPlaces)):
                if places[i].get('place_id') == hidedPlaces[j].place_id:
                    flag = True
            if not flag:
                sortedPlaces.append(places[i])
        
        likedPlaces = dbWorker.getLikedPlaces(user.id)        
        for i in range(len(sortedPlaces)):
            flag = False
            for j in range(len(likedPlaces)):
                if sortedPlaces[i].get('place_id') == likedPlaces[j].place_id:
                    flag = True
                if flag:
                    sortedPlaces[i]['liked'] = True

        return render_template('index.html', places=sortedPlaces, auth=True, user=user)

    elif request.method == 'POST':
        places = api.getPlaces(prepareRequest.prepareList(request.form))
        if not auth.isLoggedUser(request.cookies):
            return render_template('index.html', places=places, auth=False, keyword=request.form.get('keyword'))
        user = dbWorker.getUser(request.cookies.get('userLogin'))
        sortedPlaces = []

        hidedPlaces = dbWorker.getHidedPlaces(user.id)
        for i in range(len(places)):
            flag = False
            for j in range(len(hidedPlaces)):
                if places[i].get('place_id') == hidedPlaces[j].place_id:
                    flag = True
            if not flag:
                sortedPlaces.append(places[i])
        
        likedPlaces = dbWorker.getLikedPlaces(user.id)        
        for i in range(len(sortedPlaces)):
            flag = False
            for j in range(len(likedPlaces)):
                if sortedPlaces[i].get('place_id') == likedPlaces[j].place_id:
                    flag = True
                if flag:
                    sortedPlaces[i]['liked'] = True

        return render_template('index.html', places=sortedPlaces, auth=True, user=user, keyword=request.form.get('keyword'))

@app.route('/place/<placeId>')
def place(placeId=None):

    user = None
    liked = None
    hided = None

    if placeId:
        currentuser = dbWorker.getUser(request.cookies.get('userLogin'))
        if currentuser:
            user = currentuser
            isLiked = dbWorker.getLikedPlace(placeId, user.id)
            if isLiked:
                liked = True
            isHided = dbWorker.getHidedPlace(placeId, user.id)
            if isHided:
                hided = True
        print(liked)
        print(hided)
        place = api.getPlaceInfo(prepareRequest.preparePlaceInfo(placeId))
        return render_template('place.html', place=place, auth=True, user=user, liked=liked, hided=hided)
    else:
        return redirect(url_for('index'))


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
        

@app.route('/like/<placeId>')
def like(placeId = None):
    if placeId:
        user = dbWorker.getUser(request.cookies.get('userLogin'))
        dbWorker.addLikedPlace(placeId, user.id)
    return redirect(url_for('index'))


@app.route('/hide/<placeId>')
def hide(placeId = None):
    if placeId:
        user = dbWorker.getUser(request.cookies.get('userLogin'))
        dbWorker.addHidedPlace(placeId, user.id)
    return redirect(url_for('index'))

@app.route('/hided')
def hided():
    if not auth.isLoggedUser(request.cookies):
        return redirect(url_for('index'))

    user = dbWorker.getUser(request.cookies.get('userLogin'))
    hidedPlacesIds = dbWorker.getHidedPlaces(user.id)

    places = []
    
    for place in hidedPlacesIds:
        place = api.getPlaceInfo(prepareRequest.preparePlaceInfo(place.place_id))
        places.append(place)

    return render_template('hided.html', places=places, auth=True, user=user)

@app.route('/liked')
def liked():
    if not auth.isLoggedUser(request.cookies):
        return redirect(url_for('index'))

    user = dbWorker.getUser(request.cookies.get('userLogin'))
    likedPlacesIds = dbWorker.getLikedPlaces(user.id)
    for i in likedPlacesIds:
        print(i.place_id)
    places = []
    
    for place in likedPlacesIds:
        place = api.getPlaceInfo(prepareRequest.preparePlaceInfo(place.place_id))
        places.append(place)

    return render_template('liked.html', places=places, auth=True, user=user)

@app.route('/removefromhidden/<placeId>')
def removefromhidden(placeId = None):
    if placeId:
        user = dbWorker.getUser(request.cookies.get('userLogin'))
        dbWorker.removeHidedPlace(placeId, user.id)

    return redirect(url_for('hided'))

@app.route('/removefromliked/<placeId>')
def removefromliked(placeId = None):
    if placeId:
        user = dbWorker.getUser(request.cookies.get('userLogin'))
        dbWorker.removeLikedPlace(placeId, user.id)

    return redirect(url_for('liked'))

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('userID', '', expires=0)
    resp.set_cookie('userLogin', '', expires=0)
    return resp