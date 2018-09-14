#Copyright 2018 Nathan Wiebe nwiebe@bu.edu
#EC 601 Mini Project 1 Google Vision Module

import io
import os
from google.cloud import vision
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
		if ((len(newlabel[linecount]) + len(label.description)) < 39):
			newlabel[linecount] = newlabel[linecount] + label.description + ", "
		else:
			linecount = linecount + 1
			labeln = label.description + ", "
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

#The code for getlabels is mostly copied from Google vision documentation.
#https://cloud.google.com/vision/docs/detecting-labels#vision-label-detection-python
def getlabels(imgstr):
	#Location of authentication file. Stored outside Git path for security.
	authfile = "/home/nathan/Documents/EC601/Project1/googlekeys.json"

	#Initialize client.
	client = vision.ImageAnnotatorClient.from_service_account_json(authfile)

	#Open image.
	with io.open(imgstr, 'rb') as image_file:
		content = image_file.read()

	#Analyze image.
	image = vision.types.Image(content=content)
	response = client.label_detection(image=image)

	#Get labels.
	labels = response.label_annotations

	print('Labels:')

	#Turn individual labels into neat lines.
	label = stringfix(labels)

	return label
