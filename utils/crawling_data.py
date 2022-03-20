import tweepy
import pandas as pd
import datetime

def auth():
    access_token = "2166387362-iHdudntiQe9Yi8a028bUT1jf9bIqxER2Wm5or2R"
    access_token_secret = "6N9r4MgeBND9bO3KFBmiiDQgXDpIDt0vyGgK6QkR25my7"
    api_key = "g1L1qvTUFJv7mXUp9djuPJb5d"
    api_key_secret = "VLd3k673gBd8uGULpFkt44bAeMfRWK5AHn7AL0snA0CY74PP6U"
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api
    
def get_data(keyword):
    api = auth()
    search_key = keyword

    c = []
    i = []
    u = []
    t = []
    l = []
    r = []
    f = []
    v = []
    s = []

    day = 0
    while day <= 8:
        date = datetime.datetime.today()
        delta = datetime.timedelta(days=day)
        min7days = date - delta
        strtime = min7days.strftime('%Y-%m-%d')
        new_tweets = api.search_tweets(q=search_key,count=100, lang="id", until=strtime)
        for tweet in new_tweets:
                    c.append(tweet.created_at)
                    i.append(tweet.id)
                    u.append(tweet.user.screen_name)
                    t.append(tweet.text.encode("utf-8"))
                    l.append(tweet.favorite_count)
                    r.append(tweet.retweet_count)
                    f.append(tweet.user.followers_count)
                    v.append(tweet.user.verified)
                    s.append(tweet.user.statuses_count)
        day += 1            
    dictTweets = {"waktu":c, "id":i, "username":u, "tweet":t, "favorite_count": l, "retweet_count":r, "followers_count":f, "verified":v, "statuses_count":s}
    df = pd.DataFrame(dictTweets, columns=["waktu", "id", "username", "tweet", "favorite_count", "retweet_count", "followers_count", "verified", "statuses_count"])
    return df