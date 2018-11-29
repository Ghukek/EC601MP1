# EC601MP1
EC601 Mini Project 1

# Run

Once you have satisfied keys, dependencies, and databases all of which are explained in the following sections, run 

$ python TopModule.py

from your terminal.

# Keys
You will need a Google API key, stored in a json file in the parent directory to this one (outside of the git path). Name it 'googlekeys.json'.
You will need Twitter API keys as well, modify the code of 'TweetAPI.py' and change the variables to include your own keys. You should also place this file in the parent directory.

# Dependencies
You will need to install the following Python libraries using $ pip install
-tweepy
-PIL
-google-cloud-vision
-pymongo
-mysqlclient (see MySQL instructions)

You will also need to install ffmpeg.

# Mongo
You will need to install and run Mongo on your personal machine.

Use $ sudo service mongod start 

Or use an equivalent method for your operating system.

# MySQL
You will need to install and run MySQL on your personal machine.

By default, the program is not expecting to need to use a password and it will be expecting to be running on a localhost. You can change these settings in the file MP3MySQL.py.

Before running, 

$ pip install mysqlclient

make sure to install MySQL. You may also need to run 

$ sudo apt-get install libmysqlclient-dev

Or use an equivalent method for your operating system for installing Python and MySQL development headers and libraries. See https://pypi.org/project/mysqlclient/ for more details.

You will need to create a database. I am using the database name 'miniprojectdb' but you may change that in MP3MySQL.py.

# Files

# Topmodule.py

This is the main program. You should run this. It contains two functions. 

videocrator() is run when the user selects to make a new video. It manages tweet collection, image analysis, and video creation. It is self contained and if given a properly written dummy api [not currently existing], it can run without a database. It pulls from a database to reduce data usage when able.

dataanalyzer() is run when the user selects to analyze data. It calls to the database through the provided api and can return a list of top tags (as many as requested by the user) or a list of users affiliated with a tag.

# Todo
Complete ReadMe
Add MySQL api
Add No Database api

