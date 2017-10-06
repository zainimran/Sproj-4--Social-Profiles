import requests
import time
import json
from pprint import pprint
from pymongo import MongoClient

#client = MongoClient('localhost', 27017) # connecting to mongo
token = "EAACEdEose0cBABzJaElRu4cv9zSiYfiJKAPtvB3ZAXPREHKDNfgayvMXNHyhpREsSwU4lfJHpGIItezdzy16oWZAahIDa3f8ZBfvsJOYnrOdjORcGE7Nnfj04qJmHOtneVslVZBgFXwKOO1BRNq6S3O74inv2Ng205gN4P3XAsWyRJJiJJ5qmy5ZCLALKXhSmSxHZCa5y6ZAQZDZD"
req = "210354282318065?fields=posts{message,comments,likes}"

def request_fb (req): #making https request to graph api
	r = requests.get('https://graph.facebook.com/v2.9/' + req , {'access_token' : token})
	result = r.json()
	return result

#make database (start mongod first on shell)
#db = client['socialProfiles']
#posts = db['posts']

result = request_fb(req)
result = result['posts']

data = []
while True:
	try: 
		data.extend(result['data'])
		r = requests.get(result['paging']['next'])
		result = r.json()
	except:
		print 'done-posts'
		break

for p in data:
	likes_data = []
	result = p['likes'] 
	while True:
		try: 
			likes_data.extend(result['data'])
			r = requests.get(result['paging']['next'])
			result = r.json()
		except:
			print 'done-likes'
			break
	p['likes']['data'] = likes_data

pprint(data)