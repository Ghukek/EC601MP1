#Copyright 2018 Nathan Wiebe nwiebe@bu.edu
#EC 601 Mini Project 1 Top Module 

import tweepy
import os
import sys
import operator
import MP1Tweets
import MP1FFMPEG

def videocreator():
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
		sys.exit(1)
	if (urls is 0):
		print("There was an issue authorizing with Twitter, cancelling...")
		sys.exit(1)
	if (urls is 2):
		print("No tweets found. Either account is protected or there are no tweets, cancelling...")
		sys.exit(1)
	if (len(urls) is 0):
		if lasttweet == -1:
			print("No images found, cancelling...")
			sys.exit(1)
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
				print("No video to create, cancelling...")
				sys.exit(1)

	#Send image urls to retrieve images.
	imgres, labels = MP1Tweets.retrieve(urls, oldimgurls, oldlabels)

	#Error checking results of retrieve function.
	if (imgres == -1):
		print("./ImageDump folder could not be deleted, cancelling...")
		sys.exit(1)
	if (imgres == -2):
		print("Google Vision API unable to authenticate, cancelling...")
		sys.exit(1)
	else:
		print("Images retrieved successfully...")

	#Send to FFMPEG module.
	MP1FFMPEG.jpegtompeg(imgres, uname)

	# Post to db
	if lasttweet == -1:
		postres = dbapi.postnewdata(uname, maxtweet, urls, labels)
	else:
		postres = dbapi.updatedata(uname, maxtweet, urls, labels)

def dataanalyzer():
	print("\nPlease enter a search tag.")
	req = str(input("Press T for tag ranks. Press S to stop: "))
	while True:
		if (req is "s" or req is "S"):
			break
		elif (req is "d" or req is "D"):
			num = input("What number of top tags do you want to see? Input a number: ")
			try:
				num = int(num)
				dic = dbapi.findalltags()
				sorted_dic = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
				if num > len(sorted_dic):
					num = len(sorted_dic)
				for i in range(0, num):
					print("Tag #%d: ""%s"". Occurances: %d" % (i + 1, sorted_dic[i][0], sorted_dic[i][1]))
			except ValueError:
				print("You did not enter a number.")
			print("\nPlease enter another search tag.")
			req = str(input("Press T for tag ranks. Press S to stop: "))
		else:
			userlist = dbapi.findstring(req)
			if not userlist:
				print("Tag not found.")
			else:
				print("Users with images containing tag: ")
				for user in userlist:
					print(user)
			print("\nPlease enter another search tag.")
			req = str(input("Press T for tag ranks. Press S to stop: "))

print("Welcome!")

# Once I implement the MySQL API, I will make this an option.
print("\nPlease choose your database.")
req = str(input("Press M for MongoDB. Press S for MySQL: "))
while True:
	if (req is "M" or req is "m"):
		import MP3Mongo as dbapi
		break
	elif (req is "S" or req is "s"):
		print("MySQL not implmented, cancelling...")
		sys.exit(2)
	else:
		req = str(input("Please input M or S: "))

req = str(input("\nPress N to make a new video. Press A to analyze data: "))
while True:
	if (req is "a" or req is "n" or req is "A" or req is "N"):
		break
	else:
		req = str(input("Please input N or A: "))

if (req is "a" or req is "A"):
	dataanalyzer()
else:
	videocreator()

print("Everything completed successfully. Re-run the program if you wish to do more.")
print("Goodbye!")