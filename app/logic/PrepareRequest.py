class PrepareRequest:

    placesRequest = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=51.657492, 39.204741&radius=1500&'
    placeRequest = 'https://maps.googleapis.com/maps/api/place/details/json?language=ru&placeid={}&key='

    def prepareList(self, post):

        print(post)

        params = {}
        
        if post.get('type'):
            params['type'] = post.get('type')
        else:
            params['type'] = 'cafe'
        
        params['language'] = 'ru'

        if post.get('keyword'):
            params['keyword'] = post.get('keyword')
        else:
            params['keyword'] = ''
        
        if post.get('kitchen'):
            params['keyword'] = params.get('keyword') + ' ' + post.get('kitchen')

        if post.get('min_price'):
            params['minprice'] = post.get('min_price')

        if post.get('max_price'):
            params['maxprice'] = post.get('max_price')

        if post.get('open_now'):
            params['opennow'] = ''

        tmpRequest = '{}'.format(self.placesRequest)

        for i in params:
            tmpRequest += '{}={}&'.format(i, params[i])

        return tmpRequest


    
    def preparePlaceInfo(self, placeId):
        return self.placeRequest.format(placeId)
