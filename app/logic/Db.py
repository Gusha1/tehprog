from models.entity.hide import  Hide
from models.entity.like import Like
from models.entity.user import User

class Db:

    def getUser(self, username, password):
        pass


    def addUser(self, username, password):
        pass


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
