#Copyright 2018 Nathan Wiebe
#EC 601 Mini Project 1 TweetGrabber

import tweepy
import os

def grab(handle):
	consumer_key = ""
	consumer_secret = ""
	access_key = ""
	access_secret = ""


	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	print("TweetGrab Called")
	tweetlist = []

	newtweet = api.user_timeline(screen_name = handle, count=1)
	print(newtweet[0].id)

	while len(newtweet) > 0:
		newid = newtweet[0].id - 1
		tweetlist.extend(newtweet)
		newtweet = api.user_timeline(screen_name = handle,count=1,max_id=newid)
		print(newtweet[0].id)


def parse():
	print("TweetParse Called")