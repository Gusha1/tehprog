import requests
from datetime import datetime

class API:

    KEY = 'AIzaSyDooChPPBphAwvteQu6L0qVwO-jScoDXoQ'

    def getPlaces(self, query):
        placesResponse = requests.get(query + self.KEY)

        places = placesResponse.json()

        res = []

        for place in places.get('results'):
            tmp = {}
            if 'photos' in place:
                photo = place.get('photos')[0]
                photo = 'https://maps.googleapis.com/maps/api/place/photo?photoreference={}&maxwidth=600&key={}'.format(photo.get('photo_reference'), self.KEY)
                tmp['photo'] = photo
            else:
                tmp['photo'] = 'https://c-lj.gnst.jp/public/img/common/noimage.jpg?20181125050042'

            if 'rating' in place:
                rating = place.get('rating')
                if int(rating) < rating:
                    tmp['rating'] = int(rating)
                    tmp['rating_decimal'] = True
                else:
                    tmp['rating'] = int(rating)
                    tmp['rating_decimal'] = True
            
            if 'vicinity' in place:
                tmp['address'] = place['vicinity']
            
            tmp['name'] = place.get('name')
            tmp['href'] = '/place/{}'.format(place.get('place_id'))
            tmp['place_id'] = place.get('place_id')

            res.append(tmp)

        return res

    def getPlaceInfo(self, query):
        placeResponse = requests.get(query + self.KEY)
        place = placeResponse.json()
        place = place.get('result')

        res = {}
        
        res['name'] = place.get('name')
        res['place_id'] = place.get('place_id')

        if 'opening_hours' in place:
            if 'open_now' in place.get('opening_hours'):
                res['open_now'] = True
            if 'weekday_text' in place.get('opening_hours'):
                opening_hours = place.get('opening_hours')
                res['weekday_text'] = opening_hours.get('weekday_text')
        
        if 'photos' in place:
            photo = place.get('photos')[0]
            res['photo'] = 'https://maps.googleapis.com/maps/api/place/photo?photoreference={}&maxwidth=600&key={}'.format(photo.get('photo_reference'), self.KEY)
        else:
            res['photo'] = 'https://c-lj.gnst.jp/public/img/common/noimage.jpg?20181125050042'
        
        if 'rating' in place:
            rating = int(place.get('rating'))
            if rating < place.get('rating'):
                res['rating'] = rating
                res['rating_decimal'] = True
            else:
                res['rating'] = rating
                res['rating_decimal'] = False

        if 'reviews' in place:
            requestReviews = place.get('reviews')
            reviews = []

            for review in requestReviews:
                tmp = {}
                if 'author_name' in review:
                    tmp['author_name'] = review.get('author_name')
                
                if 'profile_photo_url' in review:
                    tmp['profile_photo_url'] = review.get('profile_photo_url')
                
                tmp['text'] = review.get('text')
                dt_obj = datetime.fromtimestamp(review.get('time'))
                tmp['time'] = str(dt_obj)[:-9]
                reviews.append(tmp)
            
            res['reviews'] = reviews 
            
        if 'vicinity' in place:
            res['vicinity'] = place.get('vicinity')

        if 'website' in place:
            res['website'] = place.get('website')

        return res
