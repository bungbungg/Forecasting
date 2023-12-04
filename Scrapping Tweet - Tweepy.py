# -*- coding: utf-8 -*-
"""crawling data twitter

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kOgv5MdhBfQljrhbI3bZLQvhCkA3Fil2
"""

import tweepy
import re
from textblob import TextBlob
import pandas as pd
import csv

api_key             = "fiZtq8TJTHng1"
api_secret          = "SUrht0tOeMxk68xTQva"
access_token        = "968645356543082496-ww"
access_token_secret = "jy8PCnpJgd1jMt"

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api  = tweepy.API(auth, wait_on_rate_limit=True)

search        = "indosat"

csvFile       = open(search+".csv","a+",newline="",encoding="utf-8")
csvWriter     = csv.writer(csvFile)

tanggal_tweet = []
id            = []
pengguna      = []
isi_tweet     = []

for tweet in tweepy.Cursor(api.search, q=search, count=50, lang="id").items():
    print(tweet.created_at,tweet.id,tweet.user.name,tweet.text)
    tanggal_tweet.append(tweet.created_at)
    id.append(tweet.id)
    pengguna.append(tweet.user.name)
    isi_tweet.append(tweet.text)

    tweets = [tweet.created_at,tweet.id,tweet.user.name,tweet.text]
    csvWriter.writerow(tweets)

dictTweets = {"tanggal_tweet":tanggal_tweet, "id":id, "pengguna":pengguna, "isi_tweet":isi_tweet}
df = pd.DataFrame(dictTweets,columns=["tanggal_tweet","id","pengguna","isi_tweet"])
df

import string
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")

stop_words = set(stopwords.words("english"))
#print(stop_words)

from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

wordnet = WordNetLemmatizer()
def text_preproc(x):
  x = x.lower()
  x = ' '.join([word for word in x.split(' ') if word not in stop_words])
  x = x.encode('ascii', 'ignore').decode()
  x = re.sub(r'https*\S+', ' ', x)
  x = re.sub(r'@\S+', ' ', x)
  x = re.sub(r'#\S+', ' ', x)
  x = re.sub(r'\'\w+', '', x)
  x = re.sub('[%s]' % re.escape(string.punctuation), ' ', x)
  x = re.sub(r'\w*\d+\w*', '', x)
  x = re.sub(r'\s{2,}', ' ', x)
  return x

df['clean_tweet'] = df.isi_tweet.apply(text_preproc)
df

analisis  = TextBlob(df['clean_tweet'])

if analisis.sentiment.polarity > 0.0:
    tweet_properties['sentimen'] = "positif"
    #elif analisis.sentiment.polarity == 0.0:
        #tweet_properties["sentimen"] = "netral"
else:
    tweet_properties["sentimen"] = "negatif"
    print(tweet_properties)

with open(search+".csv", 'a+', newline='') as csv_file:
            fieldNames = ["pengguna", "isi_tweet"]
            writer = csv.DictWriter(csv_file, fieldnames = fieldNames, delimiter=";",)
            writer.writerow(dictTweet)