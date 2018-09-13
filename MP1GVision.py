#Copyright 2018 Nathan Wiebe nwiebe@bu.edu
#EC 601 Mini Project 1 Google Vision Module

import io
import os
from google.cloud import vision

#The code for getlabels is mostly copied from Google vision documentation.
#https://cloud.google.com/vision/docs/detecting-labels#vision-label-detection-python
def getlabels(imgstr):
	authfile = "/home/nathan/Documents/EC601/Project1/googlekeys.json"

	client = vision.ImageAnnotatorClient.from_service_account_json(authfile)

	with io.open(imgstr, 'rb') as image_file:
		content = image_file.read()

	image = vision.types.Image(content=content)
	response = client.label_detection(image=image)
	labels = response.label_annotations
	print('Labels:')

	for label in labels:
		print(label.description)

	return labels
