#Copyright 2018 Nathan Wiebe
#EC 601 Mini Project 1 Top Module 

import tweepy
import os
import MP1Tweets

print("main module called")
handle=input('Enter a Twitter Handle: ')
if handle[0] is not '@':
	print("handle incomplete: fixing")
	handle = "@" + handle
print("You chose: ", handle )

MP1Tweets.grab("null")

MP1Tweets.parse()
