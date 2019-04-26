from ..model import db

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.String(255), nullable=False)