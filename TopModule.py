#Copyright 2018 Nathan Wiebe nwiebe@bu.edu
#EC 601 Mini Project 1 Top Module 

import tweepy
import os
import MP1Tweets
import MP1FFMPEG

def main():
	print("Welcome!")

	#Get user input for Twitter handle.
	handle=input('Enter a Twitter Handle: ')

	#Check if user included the @. If not, fix.
	if handle[0] is not '@':
		print("Handle incomplete: fixing...")
		handle = "@" + handle

	print("You chose: ", handle , ".")

	#Grab tweets.
	urls = MP1Tweets.grab(handle)

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
		print("No images found, cancelling...")
		return 1

	#Send image urls to retrieve images.
	imgres = MP1Tweets.retrieve(urls)

	#Error checking results of retrieve function.
	if (imgres == -1):
		print("./ImageDump folder could not be deleted, cancelling...")
		return 1
	if (imgres == -2):
		print("Google Vision API unable to authenticate, cancelling...")
	else:
		print("Images retrieved successfully...")

	#Send to FFMPEG module.
	MP1FFMPEG.jpegtompeg(imgres)

main()