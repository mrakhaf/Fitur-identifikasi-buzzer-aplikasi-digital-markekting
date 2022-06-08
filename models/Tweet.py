from . import db 

class Tweet(db.Model):
    id = db.Column(db.String, primary_key=True),
    date = db.Column(db.Date),
    tweet = db.Column(db.String),
    like = db.Column(db.Integer),
    quote = db.Column(db.Integer),
    retweet = db.Column(db.Integer),
    id_user = db.Column(db.String),
    username = db.Column(db.String),
    followers_count = db.Column(db.Integer)