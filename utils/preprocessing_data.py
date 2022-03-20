import pandas as pd
import re

def preprocessing(data):
    df = data
    df = df.drop_duplicates(subset ="id")
    df = df[df.followers_count >= 5000]
    columns = ['x', 'y']
    clean_data = pd.DataFrame(columns=columns)
    for username, tweet in zip(df.username, df.text):
        # tweet = tweet.decode('utf-8')
        x = re.findall('@(\w+)', tweet)
        if len(x) > 1:
            for i in x:
                clean_data = clean_data.append({'x': username, 'y': i}, ignore_index=True)
        elif len(x) == 1:
            clean_data = clean_data.append({'x': username, 'y': x[0]}, ignore_index=True)

    return clean_data


