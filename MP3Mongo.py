#Copyright 2018 Nathan Wiebe nwiebe@bu.edu
#EC 601 Mini Project 1 Google Vision Module

from pymongo import MongoClient

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

    result = db.posts.find_one({'username': username})

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