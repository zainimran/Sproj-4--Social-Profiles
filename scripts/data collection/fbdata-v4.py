import requests
import time
import json
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017) # connecting to mongo
token = "EAACEdEose0cBAGf9hsLxOxyPDb6FlRbOC176YaS3ZBKbJ6tZBZAp61ZAg5kaeLdT1Y3kkaqIwFmbHjIuLVRheZCzBXORqmupFYhnTCyvP30Tw9OdrVpW35zjEtA0xlPj0ROZBm6r65AVJyZA8slfeQZCV044yys8HT6LAoxZAy7yRUQScbp4hy0RqVfrf4tnlCPwZD"
req = "NUSTOfficial?fields=id,name,likes,posts{id,message,reactions}"
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
db = client['PAGES_LIKES']
db_pages = db['Pages']

# get all posts
page = request_fb(req)
posts = page['posts']
likes = []
allposts = getAlldata(posts,'posts')

for i in range(0, 10):
	# get all reactions
	result = allposts[i]['reactions']
	reactions_data = getAlldata(result,'reactions')
	allposts[i]['reactions'] = reactions_data
	print len(likes)

	likes = list(likes)
	likes.extend(x for x in reactions_data if x not in likes)

page['posts'] = allposts
page['likes'] = likes
	
# insert post in db
db_pages.insert(page)

#pprint(post)