import pandas as pd
import re

def preprocessing(data):
    df = data
    df = df.drop_duplicates(subset ="id")
    df = df[df.followers_count >= 3000]
    columns = ['source', 'target']
    clean_data = pd.DataFrame(columns=columns)
    for username, tweet in zip(df.username, df.text):
        # tweet = tweet.decode('utf-8')
        x = re.findall('@(\w+)', tweet)
        if len(x) > 1:
            for i in x:
                clean_data = clean_data.append({'source': username, 'target': i}, ignore_index=True)
        elif len(x) == 1:
            clean_data = clean_data.append({'source': username, 'target': x[0]}, ignore_index=True)
    clean_data = (clean_data.groupby(['source', 'target']).size().sort_values(ascending=False).reset_index()).rename(columns={0:'weight'})
    return clean_data


