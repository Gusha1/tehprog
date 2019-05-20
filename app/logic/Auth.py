import hashlib
from models.entity.user import User 


class Auth:

    login = ''
    password = ''

    def login(self, username, password):
        user = User.query.filter_by(user_name=username, password=password).first()
        if user:
            return True
        else:
            return False

    def isLoggedUser(self, cookies):
        if not cookies.get('userID') or not cookies.get('userLogin'):
            return False

        user = User.query.filter_by(user_name=cookies.get('userLogin')).first()
        if not user:
            return False

        h = hashlib.sha1(str.encode(user.password))
        p = h.hexdigest()
        print(cookies.get('userID'))        
        print(p)
        return p == cookies.get('userID')
        


    def validate(self, post):
        errors = False
        if post.get('password') != post.get('password_confirm') or len(post.get('login')) < 3:
            errors = True
        
        return not errors 
        
