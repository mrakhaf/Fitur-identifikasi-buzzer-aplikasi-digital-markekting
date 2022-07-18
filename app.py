from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app,db)


# config db 
USER = 'root'
PASSWORD = ''
DATABASE = 'buzzerfinder'
# connection_name is of the format `project:region:your-cloudsql-instance`
CONNECTION_NAME = 'buzzerfinder-355616:asia-southeast2:buzzerfinder' 

SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user=USER, password=PASSWORD,
        database=DATABASE, connection_name=CONNECTION_NAME)

app.config['SQLALCHEMY_DATABASE_URI'] =  SQLALCHEMY_DATABASE_URI

# DB_NAME = 'buzzerfinder'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:@localhost/{DB_NAME}'
db.init_app(app)
db.create_all(app=app)
print('Database connected!')

import utils.preprocessing_dataV2 as preprocessing
import utils.modelling as modelling
import utils.get_data as get_data

@app.route("/")
def hello_world():
    return "Hello, This is Digital Marketing Application!"

@app.route("/buzzerfinder", methods=['POST'])
def buzzerFinder():
    keyword = request.form.get('keyword')

    #from crawling_dataV2.py
    # data = crawling.get_data(keyword)
    data = get_data.getData(keyword)

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

# @app.route("/savetweet", methods=['POST'])
# def savetweet(): 
#     from models import Tweet
#     id_tweet = request.form.get('id_tweet')
#     date = request.form.get('date')
#     tweet = request.form.get('tweet')
#     id_user = request.form.get('id_user')
#     username = request.form.get('username')
#     followers_count = request.form.get('followers_count')
#     keyword = request.form.get('keyword')
    
#     tweet = Tweet(
#         id_tweet=id_tweet, 
#         date=date, 
#         tweet=tweet, 
#         id_user=id_user, 
#         username=username, 
#         followers_count=followers_count,
#         keyword=keyword
#         )   

#     db.session.add(tweet)
#     db.session.commit()

#     data = [
#         {
#             "id_tweet": tweet.id,
#             "date": tweet.date,
#             "tweet": tweet.tweet,
#             "id_user": tweet.id_user,
#             "username": tweet.username,
#             "followers_count": tweet.followers_count,
#             "keyword": tweet.keyword,
#         }
#     ]
        
#     return {
#         "data" : data
#     }

# @app.route("/gettweetfromkeyword", methods=['POST'])
# def gettweetfromkeyword():
#     from models import Tweet 

#     keyword = request.form.get('keyword')

#     startdate = datetime.datetime.today()
#     delta = datetime.timedelta(days=8)
#     min8days = startdate - delta
#     enddate = min8days.strftime('%Y-%m-%d')
    
#     tweets = Tweet.query.filter(keyword == keyword, 
#                     Tweet.date.between(enddate, startdate)
#                     ).all()
        
#     all_tweets = []
#     for tweet in tweets:
#         data = {
#             "id": tweet.id,
#             "id_tweet": tweet.id_tweet,
#             "date": tweet.date,
#             "tweet": tweet.tweet,
#             "id_user": tweet.id_user,
#             "username": tweet.username,
#             "followers_count": tweet.followers_count,
#             "keyword": tweet.keyword,
#         }
#         all_tweets.append(data)

#     return {
#         "data": all_tweets
#     }

# @app.route("/testGetData", methods=['POST'])
# def test_get_data():
#     keyword = request.form.get('keyword')
#     data = get_data.getData(keyword)
    
#     return str(len(data))

# @app.route("/checkDate", methods=['POST'])
# def check_date():
#     keyword = request.form.get('keyword')
#     data = get_data.checkDate(keyword)
    
#     return data    

if __name__ == '__main__':
  app.run(debug=True)    