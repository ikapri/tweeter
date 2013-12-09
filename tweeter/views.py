from flask import render_template
from tweeter import app,sockets
from mongo_connection import Conn
import json
import pika

@app.route('/')
@app.route('/<int:page>')
def get_tweets(page=None):
	conn = Conn()
	data =[]
	limit = 10
	skip = 0
	if page:
		skip = 2*(page-1)		
	tweets = conn.get_tweets(skip,limit)
	for t in tweets:
		data.append(t)
	return render_template('index.html',tweets=data)

@app.route('/realtime')
def get_realtime_tweets():
	return render_template('realtime.html')

@sockets.route('/pull')
def pull_tweets(ws):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	def tweet_received(channel,method,property,body):
		ws.send(body)
	channel = connection.channel()
	channel.exchange_declare(exchange='tweets',type='fanout')
	q=channel.queue_declare(exclusive=True)
	q_name = q.method.queue
	channel.queue_bind(exchange='tweets',queue=q_name)
	channel.basic_consume(tweet_received,queue=q_name,no_ack=True)	
	channel.start_consuming()
