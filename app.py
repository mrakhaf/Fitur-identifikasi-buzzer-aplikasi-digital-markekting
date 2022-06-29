from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import utils.crawling_dataV2 as crawling
import utils.preprocessing_dataV2 as preprocessing
import utils.modelling as modelling

app = Flask(__name__)
db = SQLAlchemy()

# config db 
DB_NAME = 'buzzerfinder'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:@localhost/{DB_NAME}'
db.init_app(app)
db.create_all(app=app)
print('Database connected!')

@app.route("/")
def hello_world():
    return "Hello, This is Digital Marketing Application!"

@app.route("/buzzerfinder", methods=['POST'])
def getData():
    keyword = request.form.get('keyword')

    #from crawling_dataV2.py
    data = crawling.get_data(keyword)

    #from preprocessing.py
    clean_data = preprocessing.preprocessing(data)

    #from modelling.py
    result = modelling.modelling(clean_data)

    result = result[:10]

    return {
        "data": [
            result
        ]
    }

@app.route("/savetweet", methods=['POST'])
def savetweet(): 
    from models import Tweet
    id = request.form.get('id')
    date = request.form.get('date')
    tweet = request.form.get('tweet')
    id_user = request.form.get('id_user')
    username = request.form.get('username')
    followers_count = request.form.get('followers_count')
    keyword = request.form.get('keyword')
    
    tweet = Tweet(
        id=id, 
        date=date, 
        tweet=tweet, 
        id_user=id_user, 
        username=username, 
        followers_count=followers_count,
        keyword=keyword
        )

    # tweet = [
    #     {
    #         "id":"18922938",
    #         "tweet": "jasdgahsgdhs"
    #     }
    # ]
    

    # for tweet in tweet:
    #     print(tweet['id'])
        
    db.session.add(tweet)
    db.session.commit()


    return tweet

@app.route("/gettweetfromkeyword", methods=['POST'])
def gettweetfromkeyword():
    from models import Tweet 

    keyword = request.form.get('keyword')
    
    # tweets = Tweet.query.filter(keyword=keyword, 
    #                 db.func.date(Tweet.date)<=end, 
    #                 db.func.date(Tweet.date)>=start).all()
    
    for tweet in tweets:
        print(tweet.id)
        print(tweet.date)
        print(tweet.tweet)
        print(tweet.id_user)
        print(tweet.username)
        print(tweet.followers_count)
        print(tweet.keyword)
        print()

    return "Success get tweet"  

if __name__ == '__main__':
  app.run(debug=True)    