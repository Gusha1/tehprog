class PrepareRequest:

    placesRequest = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=51.657492, 39.204741&radius=1500&type={}&keyword={}&language=ru&key='
    placeRequest = 'https://maps.googleapis.com/maps/api/place/details/json?language=ru&placeid={}&key='

    def prepareList(self, post):
        if post.get('type'):
            placeType = post.get('type')
        else:
            placeType = 'cafe'
        
        if post.get('keyword'):
            placeKeyword = post.get('keyword')
        else:
            placeKeyword = ''

        return self.placesRequest.format(placeType, placeKeyword)


    
    def preparePlaceInfo(self, placeId):
        return self.placeRequest.format(placeId)
