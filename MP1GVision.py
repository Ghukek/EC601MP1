#Copyright 2018 Nathan Wiebe nwiebe@bu.edu
#EC 601 Mini Project 1 Google Vision Module

import io
import os
import sys
try:
	from google.cloud import vision
except ModuleNotFoundError:
	print("Please run $ pip install google-cloud-vision .")
	sys.exit(1)
import string

#Take the list of labels and put them into neat lines.
def stringfix(labels):
	#Stage list to hold each line as a string.
	newlabel = [""]

	#Linecount counter for indexing.
	linecount = 0

	#Go through input labels and combine them into strings.
	for label in labels:
		#Limit each string to 40 characters.
		if ((len(newlabel[linecount]) + len(label)) < 39):
			newlabel[linecount] = newlabel[linecount] + label + ", "
		else:
			linecount = linecount + 1
			labeln = label + ", "
			newlabel.append(labeln)

	#Stage list to hold fixed lines.
	returnlabel = []

	#Fix lines by removing trailing spaces and capitalizing letters.
	for line in newlabel:
		line = line[:-1]
		line = string.capwords(line)
		print(line)
		returnlabel.append(line)

	return returnlabel

def toarray(labels):
	returnlabel = []

	for label in labels:
		returnlabel.append(label.description)

	return returnlabel

#The code for getlabels is mostly copied from Google vision documentation.
#https://cloud.google.com/vision/docs/detecting-labels#vision-label-detection-python
def getlabels(imgstr):
	#Location of authentication file. Stored outside Git path for security.
	authfile = "/home/nathan/Documents/EC601/Project1/googlekeys.json"

	#Initialize client.
	try:
		client = vision.ImageAnnotatorClient.from_service_account_json(authfile)
	except:
		return 0

	#Open image.
	with io.open(imgstr, 'rb') as image_file:
		content = image_file.read()

	#Analyze image.
	image = vision.types.Image(content=content)
	response = client.label_detection(image=image)

	#Get labels.
	labels = response.label_annotations

	print('Labels:')

	label = toarray(labels)

	return label
