from celery import Celery
import json
from pymongo import MongoClient
from datetime import datetime
from mongo_connection import Conn

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

c = Conn()
db = c.db

@celery_app.task
def store_tweets(tweet):
    try:
    	created_at = tweet['created_at'].split(' ')
    	date_string = created_at[1]+' '+created_at[2]+' '+created_at[3]+' '+created_at[5]
    	epoch = datetime.strptime(date_string,"%b %d %H:%M:%S %Y").strftime("%s")
    	db.tweet.insert({'id':tweet['id_str'],'rt_count':tweet['retweet_count'],'text':tweet['text'],'username':tweet['user']['name'],'screen_name':tweet['user']['screen_name'],'profile_image_url':tweet['user']['profile_image_url'],'created_at':epoch})
    except Exception as e:
    	print e

