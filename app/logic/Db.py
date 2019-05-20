from models.entity.hide import  Hide
from models.entity.like import Like
from models.entity.user import User
from app import db

class Db:

    def getUser(self, username, password):
        pass

    def addUser(self, username, password):
        user = User(user_name=username, password=password)
        print('hello world')
        db.session.add(user)
        db.session.commit()


    def getLikedPlaces(self):
        pass


    def getLikedPlace(self, placeId):
        pass


    def addLikedPlace(self, placeId):
        pass


    def removeLikedPlace(self, placeId):
        pass


    def getHidedPlaces(self):
        pass


    def addHidedPlace(self, placeId):
        pass


    def removeHidedPlace(self, placeId):
        pass
