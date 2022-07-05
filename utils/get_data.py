from gridfs import Database
import tweepy
import pandas as pd
from flask import request
from decouple import config
from app import db
from models import Tweet
import datetime

def auth():
    BEARER_TOKEN = config('BEARER_TOKEN')
    client = tweepy.Client(BEARER_TOKEN)
    return client

def getFromDB(keyword, date):
    
    if date != '':
        date = date.split('-')
        startdate = datetime.date(int(date[0]), int(date[1]), int(date[2]))
    else : 
        startdate = datetime.datetime.today()

    delta = datetime.timedelta(days=8)
    min8days = startdate - delta
    enddate = min8days.strftime('%Y-%m-%d')

    tweets = Tweet.query.filter(Tweet.keyword == keyword, 
                    Tweet.date.between(enddate, startdate)
                    ).all()
        
    columns = [
            "id",
            "date",
            "text",
            "author_id",
            "username",
            "followers_count"
        ]

    tweets_data = []
    for tweet in tweets:
        data = {
            "id": tweet.id_tweet,
            "created_at": tweet.date,
            "text": tweet.text,
            "author_id": tweet.id_user,
            "username": tweet.username,
            "followers_count": tweet.followers_count
        }
        tweets_data.append(data)

    data_tweets = pd.DataFrame(tweets_data, columns=columns)

    return data_tweets     

def get_data_api_twitter(keyword, date):
    client = auth()
    tweets_data = []
    tweets_user = []
    keyword += " lang:id"
    if date != '' :
        date = date.split('-')
        date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        date = date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"Z"
        for response in tweepy.Paginator(client.search_recent_tweets,
                                    query=keyword,
                                    start_time=date,
                                    # end_time=date,
                                    tweet_fields = ["created_at", "author_id", "text"],
                                    user_fields = ["name", "username", "location", "verified", "description", "public_metrics"],
                                    max_results = 100,
                                    expansions='author_id', limit=500):
            tweets_data += response.data
            tweets_user += response.includes["users"]
    else : 
        for response in tweepy.Paginator(client.search_recent_tweets,
                                        query=keyword,
                                        # start_time=date,
                                        # end_time=time,
                                        tweet_fields = ["created_at", "author_id", "text"],
                                        user_fields = ["name", "username", "location", "verified", "description", "public_metrics"],
                                        max_results = 100,
                                        expansions='author_id', limit=500):
            tweets_data += response.data
            tweets_user += response.includes["users"]    

    tweet_data = []
    for tweet in tweets_data:
        tweet_info = {
            'id': tweet.id,
            'author_id': tweet.author_id,
            'created_at': tweet.created_at,
            'text': tweet.text,
        }
        tweet_data.append(tweet_info)

    data_tweet = pd.DataFrame(tweet_data)

    users_data = []
    for user in tweets_user:
        user_info = {
            'id_user': user.id,
            'username': user.username,
            'followers_count': user.public_metrics['followers_count']
        }
        users_data.append(user_info)

    data_user = pd.DataFrame(users_data)  
    raw_data = pd.merge(data_tweet, data_user, how='left', left_on='author_id', right_on='id_user')
    return raw_data  

def getData(keyword):
    #get from databases 
    date = checkDate(keyword)
    data = getFromDB(keyword, date) 
 
    #check 
    if len(data) > 0 :
        if date == '':
            print('get from db!')
            data_tweets = data
        else :
            print("get data from db and request api!")
            data_tweets = get_data_api_twitter(keyword, date)

            #save to db
            tweets = data_tweets.drop_duplicates(subset='id')
            for id, created_at, text, id_user, username, followers_count in zip(tweets.id, tweets.created_at, tweets.text, tweets.id_user, tweets.username, tweets.followers_count,):
                tweet = Tweet(
                    id_tweet=id, 
                    date=created_at, 
                    text=text, 
                    id_user=id_user, 
                    username=username, 
                    followers_count=followers_count,
                    keyword=keyword
                    )   

                db.session.add(tweet)
                db.session.commit()
            date = ""    
            data_tweets = getFromDB(keyword, date)

    else:
        print('get from request api!')
        date = ""
        data_tweets = get_data_api_twitter(keyword, date)

        #save to db
        tweets = data_tweets.drop_duplicates(subset='id')
        for id, created_at, text, id_user, username, followers_count in zip(tweets.id, tweets.created_at, tweets.text, tweets.id_user, tweets.username, tweets.followers_count,):
            tweet = Tweet(
                id_tweet=id, 
                date=created_at, 
                text=text, 
                id_user=id_user, 
                username=username, 
                followers_count=followers_count,
                keyword=keyword
                )   

            db.session.add(tweet)
            db.session.commit()
        data_tweets = getFromDB(keyword, date)

    return data_tweets 

def checkDate(keyword):
    day = 7
    date_today = datetime.date.today()
    while day >= 0:
        delta = datetime.timedelta(days=day)
        date_check = date_today - delta
        strtime = date_check.strftime('%Y-%m-%d')
        time1 = (datetime.time(00, 00, 00)).strftime("%H:%M:%S")
        time2 = (datetime.time(23, 59, 59)).strftime("%H:%M:%S")
        tweets = Tweet.query.filter(Tweet.keyword == keyword, 
                    Tweet.date.between((strtime + " " + time1), (strtime + " " + time2))
                    ).all()
        date_not_found = ''                       
        if len(tweets) > 0 :
            print(strtime + " ada!")
        else :
            print(strtime + " tidak ada")
            date_not_found = strtime   
            day = 0 
        day -= 1

    return date_not_found

# def checkData(keyword):
#     keyword = request.form.get('keyword')

#     tweets = Tweet.query.filter_by(keyword=keyword).all()

#     # check database
#     if tweets:
#         day = 0
#         date = datetime.datetime.today()
#         while day <= 8:
#             delta = datetime.timedelta(days=day)
#             min7days = date - delta
#             strtime = min7days.strftime('%Y-%m-%d')
#             for tweet in tweets:
#                 # check date
#                 if (tweet.date == strtime):
#                     pass
#             day += 1
#     return tweets        



