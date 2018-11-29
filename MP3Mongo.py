#Copyright 2018 Nathan Wiebe nwiebe@bu.edu
#EC 601 Mini Project 1 Mongo DB module

import sys
try:
    from pymongo import MongoClient
except ModuleNotFoundError:
    print("Please run $ pip install pymongo .")
    sys.exit(1)

# Establish connection with default Mongo Client.
client = MongoClient()

# Access MP3 database.
db = client.miniprojectdb

def postnewdata(username, lasttweet, imgurllist, taglist):
    """Used to create a new user."""

    post_data = {
        'username': username,
        'lasttweet': lasttweet,
        'imgurllist': imgurllist,
        'taglist': taglist,
    }
    result = db.posts.insert_one(post_data)
    
    return(result.acknowledged)

def checkdata(username):
    """Gets the most recent tweet found by the database for given user."""
    # If user is not in database, return -1.

    try:
        result = db.posts.find_one({'username': username})
    except:
        print("Could not connect to your Mongo Server.")
        sys.exit(1)

    if result:
        return(result['lasttweet'], result['imgurllist'], result['taglist'])
    else:
        return(-1, [], [])

def updatedata(username, lasttweet, imgurllist, taglist):
    """Used to update user data in db."""
    tempdoc = db.posts.find_one({'username': username})

    newilist = imgurllist + tempdoc['imgurllist']
    newtlist = taglist + tempdoc['taglist']

    result = db.posts.find_one_and_update({'username': username}, 
                                          {'$set': {'lasttweet': lasttweet,
                                                    'imgurllist': newilist,
                                                    'taglist': newtlist}})

    return 0

def findstring(string):
    """Used to return data about a certain tag within the database."""
    result = db.posts.find({'taglist':{"$elemMatch":{"$elemMatch":{"$in":[string]}}}})

    returnarray = []

    for user in result:
        returnarray.append(user['username'])

    return returnarray

def findalltags():

    result = db.posts.find()

    returndic = {}

    for user in result:
        for image in user['taglist']:
            for tag in image:
                if tag not in returndic:
                    returndic[tag] = 1
                else:
                    returndic[tag] = returndic[tag] + 1

    return returndic

def finishup():
    client.close()

    return 0

