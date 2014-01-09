import requests
import helper
import config
import json
from celery_tasks import store_tweets,publish

oauth_params = helper.get_oauth_params(config.APP_KEY,config.ACCESS_TOKEN)
headers = helper.create_auth_header(oauth_params)
tries = None

try:
	r = requests.post(config.BASE_URL,headers=headers,data=config.FORM_DATA,stream=True)
	for index,line in enumerate(r.iter_lines()):
		if tries and index == tries:
			break
		if line:
			print "Fetched..............!"
			d=json.loads(line)
			store_tweets.delay(d)
			publish.delay(d)
except Exception as e:
	print e
			
