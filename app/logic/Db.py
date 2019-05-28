from models.entity.hide import  Hide
from models.entity.like import Like
from models.entity.user import User
from app import db

class Db:

    def getUser(self, username):
        return User.query.filter_by(user_name=username).first()
        

    def addUser(self, username, password):
        user = User(user_name=username, password=password)
        print('hello world')
        db.session.add(user)
        db.session.commit()


    def getLikedPlaces(self, userId):
        return Like.query.filter_by(user_id=userId).all()


    def getLikedPlace(self, placeId, userId):
        return Like.query.filter_by(place_id=placeId, user_id=userId).first()
        


    def addLikedPlace(self, placeId, userId):
        likedPlace = Like(place_id=placeId, user_id=userId)
        db.session.add(likedPlace)
        db.session.commit()


    def removeLikedPlace(self, placeId, userId):
        Like.query.filter_by(place_id=placeId, user_id=userId).delete()
        db.session.commit()


    def getHidedPlaces(self, userId):
        return Hide.query.filter_by(user_id=userId).all()


    def addHidedPlace(self, placeId, userId):
        hidedPlace = Hide(place_id=placeId, user_id=userId)
        db.session.add(hidedPlace)
        db.session.commit()

    def getHidedPlace(self, placeId, userId):
        return Hide.query.filter_by(place_id=placeId, user_id=userId).first()

    def removeHidedPlace(self, placeId, userId):
        Hide.query.filter_by(place_id=placeId, user_id=userId).delete()
        db.session.commit()
