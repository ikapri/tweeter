from pymongo import MongoClient
import config

class Conn():
	def __init__(self,host=None,port=None):
		self.conn = MongoClient(host=host,port=port)
		self.db = self.conn[config.DB]
		self.collection = self.db[config.FORM_DATA['track'].replace('#','').lower()]
	def get_tweets(self,skip,limit):
		return self.collection.find(fields={'_id':False}).sort('created_at',-1).skip(skip).limit(limit)	
