#Copyright 2018 Nathan Wiebe nwiebe@bu.edu
#EC 601 Mini Project 1 Top Module 

import tweepy
import os
import MP1Tweets
import MP1FFMPEG

def main():
	print("Welcome!")

	# Once I implement the MySQL API, I will make this an option.
	import MP3Mongo as dbapi

	# Get user input for Twitter handle.
	handle=input('Enter a Twitter Handle: ')

	# Check if user included the @. If not, fix.
	if handle[0] is not '@':
		print("Handle incomplete: fixing...")
		handle = "@" + handle

	print("You chose: " + handle)

	# Convert handle to standard username for db.
	uname = handle[1:].lower()
	
	# Test if username is already in db.
	lasttweet, oldimgurls, oldlabels = dbapi.checkdata(uname)
	print(lasttweet)

	#Grab tweets.
	urls, maxtweet = MP1Tweets.grab(handle, lasttweet)
	print(maxtweet)

	# # url set used for testing modules without accessing API unnecessarily
	# urls = ['http://pbs.twimg.com/media/CmyXY4jWcAAt9J5.jpg', 
	# 'http://pbs.twimg.com/media/Cj-LSpNVAAEz8GS.jpg', 
	# 'http://pbs.twimg.com/media/CcfmB1wWwAA3HAj.jpg', 
	# 'http://pbs.twimg.com/media/CcfmB1wWwAA3HAj.jpg', 
	# 'http://pbs.twimg.com/media/CcbOI8aUAAARp3b.jpg']

	#Error checking results of grab function.
	if (urls is 1):
		print("Username doesn't exist, cancelling...")
		return 1
	if (urls is 0):
		print("There was an issue authorizing with Twitter, cancelling...")
		return 1
	if (urls is 2):
		print("Could not retrieve tweets, perhaps the account is protected, cancelling...")
		return 1
	if (len(urls) is 0):
		if lasttweet == -1:
			print("No images found, cancelling...")
			return 1
		else:
			conf = str(input("No new images found, do you want to make a new video from old photos? y/n: "))
			while True:
				if (conf is "y" or conf is "n" or conf is "Y" or conf is "N"):
					break
				else:
					conf = str(input("Please input y or n: "))
			if (conf is "y" or conf is "Y"):
				pass
			else:
				return(1)

	#Send image urls to retrieve images.
	imgres, labels = MP1Tweets.retrieve(urls, oldimgurls, oldlabels)

	#Error checking results of retrieve function.
	if (imgres == -1):
		print("./ImageDump folder could not be deleted, cancelling...")
		return 1
	if (imgres == -2):
		print("Google Vision API unable to authenticate, cancelling...")
	else:
		print("Images retrieved successfully...")

	#Send to FFMPEG module.
	MP1FFMPEG.jpegtompeg(imgres, uname)

	# Post to db
	if lasttweet == -1:
		postres = dbapi.postnewdata(uname, maxtweet, urls, labels)
	else:
		postres = dbapi.updatedata(uname, maxtweet, urls, labels)

main()