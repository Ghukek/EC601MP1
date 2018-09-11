#Copyright 2018 Nathan Wiebe
#EC 601 Mini Project 1 TweetGrabber

import tweepy
import os
import json

def grab(handle):
	consumer_key = "-"
	consumer_secret = "-"
	access_key = "-"
	access_secret = "-"


	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	print("TweetGrab Called")
	tweetlist = []

	newtweet = api.user_timeline(screen_name = handle, count=1)

	while len(newtweet) > 0:
		print(newtweet[0].id)
		newid = newtweet[0].id - 1
		if hasattr(newtweet[0], 'retweeted_status'):
			print("is retweet")
			if "media" in newtweet[0].retweeted_status.entities:
				print("retweet has image")
				tweetlist.extend(newtweet)
		if "media" in newtweet[0].entities:
			print("has image")
			tweetlist.extend(newtweet)
		newtweet = api.user_timeline(screen_name = handle,count=1,max_id=newid)

	writeto = open('tweetdump.json', 'w') 
	print ("Writing to file")
	for tweet in tweetlist:
		json.dump(tweet._json,writeto,sort_keys = True,indent = 4)

	writeto.close()


def parse():
	print("TweetParse Called")

	pullfrom = open('tweetdump.json', 'r')
