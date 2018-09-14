#Copyright 2018 Nathan Wiebe nwiebe@bu.edu
#EC 601 Mini Project 1 FFMPEG Module

import os
from PIL import Image, ImageDraw, ImageFont
import math

def resolutionfix(imgstr):
	print("Fixing image resolution...")

	#Open bacground and foreground images.
	base = Image.open("../000.jpg")
	front = Image.open(imgstr)

	#Check foreground image to make sure it's not too big.
	if (front.size[0] > base.size[0] or front.size[1] > base.size[1]):
		print("Image too large, resizing...")
		#Check the ratios between the foreground and background images.
		ratiow = base.size[0]/front.size[0]
		ratioh = base.size[1]/front.size[1]
		#Decide which dimension to resize based on which ratio is smaller.
		#Other dimension is resized proportionally.
		if ratiow < ratioh:
			newh = int(ratiow*front.size[1])
			neww = base.size[0]
		else:
			neww = int(ratioh*front.size[0])
			newh = base.size[1]
		#Resize based on dimensions decided.
		front = front.resize([neww, newh])

	#Find the center of the images.
	basecenter = [int(base.size[0]/2), int(base.size[1]/2)]
	frontcenter = [int(front.size[0]/2), int(front.size[1]/2)]

	#Find the upper right corner position of a centered pasted foreground image.
	centerpos = [basecenter[0]-frontcenter[0], basecenter[1]-frontcenter[1]]

	#Paste the foreground image in the background image centered according to calcs.
	combined = base.paste(front, box=centerpos, mask = None)

	#Save image.
	base.save(imgstr)

	print("Image is now 1920x1080 pixels...")

#Original code for this module copied from Pillow documentation.
#https://pillow.readthedocs.io/en/3.0.x/reference/ImageDraw.html
def stringadd(str, imgstr):
	print("Adding lables...")

	#Get an image.
	base = Image.open(imgstr).convert('RGBA')

	#Make a blank image for the text, initialized to transparent text color.
	txt = Image.new('RGBA', base.size, (255,255,255,0))

	#Get a font.
	fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)

	#Get a drawing context.
	d = ImageDraw.Draw(txt)

	if (len(str) > 0):
		#Draw text, line 1.
		d.text((520,900), str[0], font=fnt, fill=(255,255,255,255))
	if (len(str) > 1):
		#Draw text, line 2.
		d.text((520,960), str[1], font=fnt, fill=(255,255,255,255))
	if (len(str) > 2):
		#Draw text, line 3.
		d.text((520,1020), str[2], font=fnt, fill=(255,255,255,255))
	#If there are more than 3 lines of labels, ignore them.

	#Combine.
	out = Image.alpha_composite(base, txt)

	#Convert back to RGB to save as JPG.
	outjpg = out.convert("RGB")

	#Save.
	outjpg.save(imgstr)

	print("Labels added...")

def jpegtompeg(imgnum):
	print("Making slideshow...")

	#Run console command with ffmpeg settings.
	os.system("ffmpeg -loglevel panic -framerate .5 -i %03d.jpg slideshow.mp4 -vf format=yuv420p")

	print("Slideshow created with %d images..." % imgnum)