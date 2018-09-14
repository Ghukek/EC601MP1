#Copyright 2018 Nathan Wiebe nwiebe@bu.edu
#EC 601 Mini Project 1 Twitter Module

import tweepy
import os
import json
import shutil
import urllib.request
import MP1FFMPEG
import MP1GVision

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

	#Check known Twitter handle to verify authorization.
	try:
		api.get_user("@ghukek")
	except:
		return 0

	print("Checking twitter handle...")

	#Check for handle existence.
	try:
		api.get_user(handle)
	except:
		return 1

	print("Collecting tweets...")

	#Stage variable for storing urls.
	imageurls = []

	#Get first tweet. If there is an error, the account may be protected.
	try:
		newtweet = api.user_timeline(screen_name = handle, count=1)
	except:
		return 2

	tweetnum = 1
	dbleimgcheck = 0

	#Loop through tweets until no more tweets or 500 tweets have been investigated.
	#Limit for status request is 900.
	#To avoid hitting the Google Vision 1k image limit, restrict images pulled to 60.
	while (len(newtweet) > 0 and tweetnum < 501 and len(imageurls) < 61):
		print("Tweet found: ", newtweet[0].id)
		#Check if the current tweet is a retweet.
		if hasattr(newtweet[0], 'retweeted_status'):
			print("...is retweet")
			#Check if original tweet has image.
			if "media" in newtweet[0].retweeted_status.entities:
				print("...retweet has image")
				#Add image url to list.
				imageurls.append(newtweet[0].retweeted_status.entities['media'][0]['media_url'])
				#Sometimes both the retweet and the tweet contain the same image.
				#Use a check to prevent the image from saving twice.
				dblimgcheck = 1
		#Check if tweet contains image.
		if "media" in newtweet[0].entities and dblimgcheck is 0:
			print("...has image")
			#Add image url to list.
			imageurls.append(newtweet[0].entities['media'][0]['media_url'])
		#Get ready to call next tweet by reducing the id value.
		newid = newtweet[0].id - 1
		#Reset double image check.
		dblimgcheck = 0
		#Get new tweet.
		newtweet = api.user_timeline(screen_name = handle,count=1,max_id=newid)
		#Add to tweet number.
		tweetnum = tweetnum +1

	if tweetnum is 500:
		print("Max tweets collected.")
	else:
		print("All tweets collected.")

	return(imageurls)


def retrieve(imageurls):
	print("Checking ./ImageDump folder...")

	#Check if folder already exists from previous instance of this program.
	if os.path.isdir("./ImageDump"):
		#Confirm deletion.
		print("./ImageDump exists; to proceed it must be deleted which will erase all contents.")
		delconf = str(input("Confirm deletion of ./ImageDump y/n: "))
		while True:
			if (delconf is "y" or delconf is "n" or delconf is "Y" or delconf is "N"):
				break
			else:
				delconf = str(input("Please input y or n: "))
		if (delconf is "y" or delconf is "Y"):
			shutil.rmtree("./ImageDump")
			print("Folder deleted, creating new one...")
		else:
			return(-1)
	else:
		print("Folder doesn't exist, creating...")

	#Create folder and move to it.
	os.mkdir("ImageDump")
	os.chdir("./ImageDump")

	#Stage values for image naming.
	imagenum = 1
	imagestr = "000"

	for image in imageurls:
		#Check for how many zeros to add in front of number.
		#Since I limit the tweet grabber to 500 tweets, 
		#no more than that number of images is expected.
		if imagenum < 10:
			imagestr = "00%s.jpg" % (imagenum)
		elif imagenum < 100:
			imagestr = "0%s.jpg" % (imagenum)
		elif imagenum < 1000:
			imagestr = "%s.jpg" % (imagenum)
		else:
			print("Too many images, stopping...")
			break
		#Try to download image, print status of each image retrieval.
		try:
			urllib.request.urlretrieve(image, imagestr)
		except:
			print("Image: %s error, cannot retrieve. Trying next image..." % (imagestr))
		else:
			print("Image: %s retrieved..." % (imagestr))
			imagenum = imagenum + 1
			#Send to GoogleVision to get labels.
			labels = MP1GVision.getlabels(imagestr)
			#Fix image resolution to 1920x1080
			MP1FFMPEG.resolutionfix(imagestr)
			#Add labels to image.
			MP1FFMPEG.stringadd(labels, imagestr)


		

	return(imagenum)
	
	
