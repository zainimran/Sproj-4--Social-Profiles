import requests
import time
import json
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017) # connecting to mongo
token = "EAACEdEose0cBABclxm1aR0ZB9wYnj0ZCcricAOoV1QSi1y6d4sERaqjQe3qdt3NtzuVkZB6GgqW7WirugH2GXxVeZC2z1LG6RsXTiTvANtf3Sn7GdSYLvr3V4ySHOAAZCTtnZBjIdbDy91ZCJPmy6wJMgZB3T4K0nK4XR1vH1aVUf2ZBn9udPAVZCDPkGzwrblAZByjVeq14KeMogZDZD"
req = "210354282318065?fields=posts{id,message,reactions,comments{id,message,reactions}}"

def request_fb (req): #making https request to graph api
	r = requests.get('https://graph.facebook.com/v2.9/' + req , {'access_token' : token})
	result = r.json()
	return result

def getAlldata (result, type): #access all pages to get all data - eg. likes, comments
	data = []
	while True:
		try: 
			data.extend(result['data'])
			r = requests.get(result['paging']['next'])
			result = r.json()
		except:
			print 'done-' + type
			break
	return data

def filter_reactions (reactions_data): #converts all reactions list to object of lists of reactions filtered
	print "=> REACTIONS: ", len(reactions_data)
	like_data = []
	love_data = []
	haha_data = []
	wow_data = []
	sad_data = []
	angry_data = []
	thankful_data = []
	
	for r in reactions_data:
		if r['type'] == "LIKE":
			like_data.append(r)
		elif r['type'] == "LOVE":
			love_data.append(r)
		elif r['type'] == "WOW":
			wow_data.append(r)
		elif r['type'] == "HAHA":
			haha_data.append(r)
		elif r['type'] == "SAD":
			sad_data.append(r)
		elif r['type'] == "ANGRY":
			angry_data.append(r)
		elif r['type'] == "THANKFUL":
			thankful_data.append(r)
	print "- Likes: ", len(like_data)
	print "- Loves: ", len(love_data)
	print "- Wows: ", len(wow_data)
	print "- Hahas: ", len(haha_data)
	print "- Sads: ", len(sad_data)
	print "- Angrys: ", len(angry_data)
	print "- Thankfuls: ", len(thankful_data)
	
	reactions = {'all':reactions_data,
	'likes':like_data,
	'loves':love_data,
	'wows':wow_data,
	'hahas':haha_data,
	'sads':sad_data,
	'angrys':angry_data,
	'thankfuls':thankful_data}
	
	return reactions

#make database (start mongod first on shell)
db = client['LUMS']
db_posts = db['Posts']

# get all posts
result = request_fb(req)
result = result['posts']
allposts = getAlldata(result,'posts')

for post in allposts:
	# get all reactions
	result = post['reactions']
	reactions_data = getAlldata(result,'reactions')
	reactions_data = filter_reactions(reactions_data)
	post['reactions'] = reactions_data

	# get all comments
	result = post['comments']
	comments_data = getAlldata(result,'comments')
	post['comments'] = comments_data

	# insert post in db
	db_posts.insert(post)

#pprint(post)