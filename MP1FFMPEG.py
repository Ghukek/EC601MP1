#Copyright 2018 Nathan Wiebe
#EC 601 Mini Project 1 FFMPEG Module

import os
from PIL import Image
import math

def resolutionfix(imgstr):
	#Check to make sure we're in ./Imagedump. Called from MP1Tweets.retrieve, 
	#which is already there, but to make the program more modular, I should add check.
	base = Image.open("../000.jpg")
	print(imgstr)
	front = Image.open(imgstr)
	if (front.size[0] > base.size[0] or front.size[1] > base.size[1]):
		ratiow = base.size[0]/front.size[0]
		ratioh = base.size[1]/front.size[1]
		if ratiow < ratioh:
			newh = int(ratiow*front.size[1])
			neww = base.size[0]
		else:
			neww = int(ratioh*front.size[0])
			newh = base.size[1]
		front = front.resize([neww, newh])
	basecenter = [int(base.size[0]/2), int(base.size[1]/2)]
	frontcenter = [int(front.size[0]/2), int(front.size[1]/2)]
	centerpos = [basecenter[0]-frontcenter[0], basecenter[1]-frontcenter[1]]
	combined = base.paste(front, box=centerpos, mask = None)
	base.save(imgstr)


def jpegtompeg(imgnum):
	#os.chdir("./ImageDump")
	os.system("ffmpeg -framerate 1 -i %03d.jpg slideshow.mp4")