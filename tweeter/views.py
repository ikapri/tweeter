from flask import render_template
from tweeter import app
from mongo_connection import Conn
import json

@app.route('/')
@app.route('/<int:page>')
def get_tweets(page=None):
	conn = Conn()
	data =[]
	limit = 10
	if not page:
		skip = 0
	else:
		skip = 2*(page-1)		
	tweets = conn.get_tweets(skip,limit)
	for t in tweets:
		data.append(t)
	return render_template('index.html',tweets=data)