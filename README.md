tweeter
=======

Pull realtime tweets using the Twitter Streaming API


Usage
-----
* collector.py is used to collect realtime tweets using twitter streaming api
* after receiving a tweet collector.py calls celery background tasks to store and publish the tweets
* flask view for realtime streaming subscribes to the publisher which is publishing realtime tweets.The view then uses flask-websockets to send the tweets to the client side
* collector.py retreives tweets for only a single hashtag.This Hashtag can be set in config.py
* mongodb is used to store the tweets
* rabbitmq is used for pub-sub.

Instructions
------------

* celery -A celery_tasks worker --loglevel=info
* python collector.py (In different shell)
* make sure rabbitmq-server is running in the background
* run the flask api : gunicorn -k flask_sockets.worker run:app

