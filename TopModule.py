#Copyright 2018 Nathan Wiebe
#EC 601 Mini Project 1 Top Module 

import tweepy
import os
import MP1Tweets

def main():
	print("Welcome!")
	handle=input('Enter a Twitter Handle: ')
	if handle[0] is not '@':
		print("Handle incomplete: fixing...")
		handle = "@" + handle
	print("You chose: ", handle , ".")

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
	if (len(urls) is 0):
		print("No images found, cancelling...")
		return 1

	#Send image urls to retrieve images.
	errstatus = MP1Tweets.retrieve(urls)

	#Error checking results of retrieve function.
	if (errstatus == 1):
		print("./ImageDump folder could not be deleted, cancelling...")
	else:
		print("Images retrieved successfully...")

main()