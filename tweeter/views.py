from flask import jsonify
from tweeter import app
from mongo_connection import Conn
import json

@app.route('/')
def latest_tweets():
	conn = Conn()
	data =[]
	tweets = conn.get_latest_tweets()
	for t in tweets:
		data.append(t)
	return json.dumps(data)
