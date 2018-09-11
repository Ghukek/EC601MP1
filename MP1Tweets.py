#Copyright 2018 Nathan Wiebe
#EC 601 Mini Project 1 TweetGrabber

import tweepy
import os
import json
import shutil
import urllib.request

def grab(handle):
	#Keys have been obfuscated manually before uploading to git.
	consumer_key = "-"
	consumer_secret = "-"
	access_key = "-"
	access_secret = "-"


	#Authorize with API.
	print("Authorizing with Twitter...")
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	print("Collecting tweets...")

	#Add check for handle existence.

	#Stage variable for storing urls.
	imageurls = []

	#Get first tweet.
	newtweet = api.user_timeline(screen_name = handle, count=1)

	tweetnum = 1

	#Loop through tweets until no more tweets or 500 tweets have been investigated.
	#Limit for status request is 900.
	while len(newtweet) > 0:
		print("Tweet found: ", newtweet[0].id)
		#Check if the current tweet is a retweet.
		if hasattr(newtweet[0], 'retweeted_status'):
			print("...is retweet")
			#Check if original tweet has image.
			if "media" in newtweet[0].retweeted_status.entities:
				print("...has image")
				imageurls.append(newtweet[0].retweeted_status.entities['media'][0]['media_url'])
		#Check if tweet contains image.
		if "media" in newtweet[0].entities:
			print("...has image")
			imageurls.append(newtweet[0].entities['media'][0]['media_url'])
		#Get ready to call next tweet by reducing the id value.
		newid = newtweet[0].id - 1
		#Get new tweet.
		newtweet = api.user_timeline(screen_name = handle,count=1,max_id=newid)
		#Check to see if tweet limit is reached.
		if tweetnum > 500
			break

	print("Max tweets collected.")

	return(imageurls)


def retrieve(imageurls):
	print("TweetParse Called")

	if os.path.isdir("./ImageDump"):
		#Insert warning and confirmation before deletion.
		shutil.rmtree("./ImageDump")

	os.mkdir("ImageDump")
	os.chdir("./ImageDump")

	imagenum = 1

	for image in imageurls:
		if imagenum < 10:
			urllib.request.urlretrieve(image, "000%s.jpg" % (imagenum))
		elif imagenum < 100:
			urllib.request.urlretrieve(image, "00%s.jpg" % (imagenum))
		elif imagenum < 1000:
			urllib.request.urlretrieve(image, "0%s.jpg" % (imagenum))
		elif imagenum < 10000:
			urllib.request.urlretrieve(image, "%s.jpg" % (imagenum))
		imagenum = imagenum + 1
	
	
