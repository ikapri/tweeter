import base64
import random
import time
from collections import OrderedDict
import urllib2
from hashlib import sha1
import hmac
import binascii
import config

def get_nonce():
    """Unique token generated for each request"""
    n = base64.b64encode(
        ''.join([str(random.randint(0, 9)) for i in range(24)]))
    return n

def get_oauth_params(app_key,access_token):
	oauth_params = {
        'oauth_timestamp': str(int(time.time())),
        'oauth_signature_method': "HMAC-SHA1",
        'oauth_version': "1.0",
        'oauth_token': access_token,
        'oauth_nonce': get_nonce(),
        'oauth_consumer_key': app_key
    }
	params_dict = {}
	params_dict.update(config.FORM_DATA)
	params_dict.update(oauth_params)
	params_string = collect_params(params_dict)
	signature_base_string = get_base_string(config.METHOD,config.BASE_URL,params_string)
	signature = get_signature(signature_base_string)
	oauth_params['oauth_signature'] = signature
	return oauth_params

def collect_params(params_dict):
	sorted_dict = OrderedDict(sorted(params_dict.items()))
	params_string = ''
	for key,value in sorted_dict.items():
		params_string +=key+'='+urllib2.quote(value)+'&'
	return params_string[:-1]

def get_base_string(method,base_url,params_string):
	signature_string = method+'&'+urllib2.quote(base_url,safe='')+'&'+urllib2.quote(params_string,safe='')
	return signature_string

def get_signature(signature_string):
	signing_key = config.APP_SECRET+'&'+config.ACCESS_TOKEN_SECRET
	hashed = hmac.new(signing_key, signature_string, sha1)
	sig = binascii.b2a_base64(hashed.digest())[:-1]
	return sig

def create_auth_header(oauth_params):
	header_string = 'OAuth '
	header = {}
	for key,value in oauth_params.items():
		header_string+=key+'='+'"'+urllib2.quote(value)+'"'+', '
	header['Authorization'] = header_string[:-2]
	return header