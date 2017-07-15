import requests 
import pandas as pd
import os, sys

token = ""
try:
	token = os.environ['FB_TOKEN']
except:
	print "Set FB_TOKEN variable"
	sys.exit(-1)

fb_pageid = "100281786832302"
postlst = []

url = "https://graph.facebook.com/v2.9/"+fb_pageid+"/posts?limit=100&access_token="+token

while(True):
	posts = requests.get(url)
	posts_json = posts.json()
	 
	for x1 in posts_json['data']:
		postlst.append(x1.get('created_time')) 
	next_page = ""
	
	try:
		next_page = posts_json['paging']['next']
		url = next_page
	except:
		break
	if not next_page: break
	print "Count: %s,  Next Page: %s" % ( len(postlst), url)    

print "\nGenerating CSV File"

df = pd.DataFrame({'dates': postlst})
df['dates'] = pd.to_datetime(df['dates'])
df['day_of_week'] = df['dates'].dt.weekday_name
df['year'] = df['dates'].dt.year
df['month'] = df['dates'].dt.month
df['count'] = 1 

df.to_csv('data.csv')


