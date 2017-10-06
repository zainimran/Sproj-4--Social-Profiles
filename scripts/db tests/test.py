import requests
import time
import json
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017) # connecting to mongo

#make database (start mongod first on shell)
db = client['FB_DATA']
db_pages = list(db['Universities'].find())

unis = ['210354282318065','135415273327','601457159883557',
		'1618369968426373','111498722271346','115753421897473',
		'140641789392100','167017563500397','129091125100',
		'159615858797']

politics = ['1509868449278769','282925128406476','246046232150591',
		'143702242358131','144494398930201','161809687351827',
		'407147312636968','103521639725365']

links = []

print db_pages
a = db_pages[0]['active_likers']
b = db_pages[1]['active_likers']
c = [val for val in a if val in b]
print c
'''
for p in db_pages:
	for q in db_pages:
		if p != q:
			c1 = p['active_likers']
			c2 = q['active_likers']
			c3 = [val for val in c1 if val in c2]
			if len(c3) != 0:
				links.append((p['id'], q['id']))
'''
print links