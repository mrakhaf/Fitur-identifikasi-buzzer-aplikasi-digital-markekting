from app import db

class Tweet(db.Model):
    id =  db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    id_tweet = db.Column(db.String)
    date = db.Column(db.DateTime)
    text = db.Column(db.String)
    id_user = db.Column(db.String)
    username = db.Column(db.String)
    followers_count = db.Column(db.Integer)
    keyword = db.Column(db.String)
