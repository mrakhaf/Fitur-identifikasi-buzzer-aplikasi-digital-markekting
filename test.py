import tweepy
import pandas as pd
import re

import utils.crawling_dataV2 as crawling 
import utils.preprocessing_data as preprocessing

# def auth():
#     bearer_token= "AAAAAAAAAAAAAAAAAAAAAF%2F%2FXwEAAAAAkM4FZuw0TVlA3drq5dO86BBuw1A%3DfnvxoF1NmMa4WAUMh6sZ50q2ZRMmhMcN74RFN7sJtT2xrlBro7"
#     client = tweepy.Client(bearer_token)
#     return client

# def get_data(keyword):
#     client = auth()

#     tweets_data = []
#     tweets_user = []
#     keyword += " lang:id"
#     for response in tweepy.Paginator(client.search_recent_tweets,
#                                     query=keyword,
#                                     # start_time="2022-03-11",
#                                     # end_time="2022-03-11T00:00:00Z",
#                                     tweet_fields = ["created_at", "author_id", "text"],
#                                     user_fields = ["name", "username", "location", "verified", "description", "public_metrics"],
#                                     max_results = 100,
#                                     expansions='author_id', limit=500):
#         tweets_data += response.data
#         tweets_user += response.includes["users"]    

#     tweet_data = []
#     for tweet in tweets_data:
#         tweet_info = {
#             'id': tweet.id,
#             'author_id': tweet.author_id,
#             'created_at': tweet.created_at,
#             'text': tweet.text,
#         }
#         tweet_data.append(tweet_info)

#     data_tweet = pd.DataFrame(tweet_data)

#     users_data = []
#     for user in tweets_user:
#         user_info = {
#             'id_user': user.id,
#             'username': user.username,
#             'followers_count': user.public_metrics['followers_count'],
#             'verified': user.verified,
#         }
#         users_data.append(user_info)

#     data_user = pd.DataFrame(users_data)  
#     raw_data = pd.merge(data_tweet, data_user, how='left', left_on='author_id', right_on='id_user')
#     return raw_data     
    
# def preprocessing(data):
#     df = data
#     df = df.drop_duplicates(subset ="id")
#     df = df[df.followers_count >= 5000]
#     columns = ['x', 'y']
#     clean_data = pd.DataFrame(columns=columns)
#     for username, tweet in zip(df.username, df.text):
#         # tweet = tweet.decode('utf-8')
#         x = re.findall('@(\w+)', tweet)
#         if len(x) > 1:
#             for i in x:
#                 clean_data = clean_data.append({'x': username, 'y': i}, ignore_index=True)
#         elif len(x) == 1:
#             clean_data = clean_data.append({'x': username, 'y': x[0]}, ignore_index=True)

#     return clean_data  
    
raw_data = crawling.get_data('#racunshopee')  
clean_data = preprocessing.preprocessing(raw_data)
print(clean_data)

# if __name__ == '__main__':
#     print(__package__)