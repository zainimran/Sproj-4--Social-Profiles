import requests
import time
import json
from pprint import pprint
from pymongo import MongoClient

unis = ['210354282318065','135415273327','601457159883557',
		'1618369968426373','111498722271346','115753421897473',
		'140641789392100','167017563500397','129091125100',
		'159615858797']

politics = ['1509868449278769','282925128406476','246046232150591',
		'143702242358131','144494398930201','161809687351827',
		'407147312636968','103521639725365']

ideoligies = ['837224243081526']

var = unis[0]

client = MongoClient('localhost', 27017) # connecting to mongo
token = "EAACEdEose0cBAElQpTAzwMl49dPnnikMVvqugSx4sMNJQhtVZBYqzJAoZA4sQJmAcxzZCXDSRxUXSVde6Iq8tjVP0fpJbUEPekgSQUHJK1WueTJcZBLhrJ3pAHtJWb4Aa5Dv6aaSs3dwonUG73itsqwE0OovcVycPcOkmBMNET1RZAa84ZC7Ct4FEX9rVZALZBsZD"
req = var + "?fields=id,name,about,likes,posts{id,name,message,message_tags,backdated_time,created_time,scheduled_publish_time,updated_time,reactions,comments}"

def request_fb (req): #making https request to graph api
	r = requests.get('https://graph.facebook.com/v2.9/' + req , {'access_token' : token})
	result = r.json()
	print "got request"
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
db = client['FB_PAGES']
db_pages = db['Political Parties']

# get the page object
page = request_fb(req)

try:
	pagelikes = page['likes']
	pagelikes_data = getAlldata(pagelikes, 'pagelikes')
	page['likes'] = pagelikes_data
except:
	page['likes'] = []

posts = page['posts']

active_likers = []
active_commentors = []

allposts = getAlldata(posts,'posts')
#print len(allposts)

for p in allposts:
	# get all reactions
	reaction = p['reactions']
	reactions_data = getAlldata(reaction,'reactions')
#	print len(reactions_data)
	allposts[i]['reactions'] = reactions_data
	# append active likers
	active_likers = list(active_likers)
	active_likers.extend(x for x in reactions_data if x not in active_likers)

	# get all comments
	try:
		comment = allposts[i]['comments']
		comments_data = getAlldata(comment, 'comments')
	except:
		continue
#	print len(comments_data)
	allposts[i]['comments'] = comments_data
	allposts[i]['commentors'] = []

	for c in comments_data:
		allposts[i]['commentors'].append(c['from'])

	# append active commentors
	active_commentors = list(active_commentors)
	active_commentors.extend(x for x in allposts[i]['commentors'] if x not in active_commentors)

# ------------------------------------------
page['posts'] = allposts
page['active_likers'] = active_likers
page['active_commentors'] = active_commentors
	
# insert page in db
db_pages.insert(page)

#pprint(post)