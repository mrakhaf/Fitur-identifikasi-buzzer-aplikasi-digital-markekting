from app import db

class Tweet(db.Model):
    id = db.Column(db.String, unique=True, primary_key=True)
    date = db.Column(db.Date)
    tweet = db.Column(db.String)
    id_user = db.Column(db.String)
    username = db.Column(db.String)
    followers_count = db.Column(db.Integer)
    keyword = db.Column(db.String)
