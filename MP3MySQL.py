#Copyright 2018 Nathan Wiebe nwiebe@bu.edu
#EC 601 Mini Project 1 MySQL module

import sys
try:
    import mysql.connector as MySQL
    from mysql.connector import errorcode
except ModuleNotFoundError:
    print("Please install python-mysql.connector.")
    sys.exit(1)

# Change parameters if necessary.
config = {
    'user': 'nathan',
    'password': '',
    'host': 'localhost',
}

DB_NAME = 'miniprojectdb'

try:
    db = MySQL.connect(**config)
except MySQL.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
    sys.exit(1)
  else:
    print(err)
    sys.exit(1)

cursor = db.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except MySQL.Error as err:
        print("Failed creating database: {}".format(err))
        sys.exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except MySQL.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        db.database = DB_NAME
    else:
        print(err)
        exit(1)

TABLES = {}
TABLES['users'] = (
    "CREATE TABLE `users` ("
    "  `username` varchar(20) NOT NULL,"
    "  `lasttweet` char(25) NOT NULL,"
    "  PRIMARY KEY (`username`)"
    ") ENGINE=InnoDB")
TABLES['users-images'] = (
    "CREATE TABLE `images` ("
    "  `image_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `username` varchar(15) NOT NULL,"
    "  `url` char(60) NOT NULL,"
    "  PRIMARY KEY (`image_no`)"
    ") ENGINE=InnoDB")
TABLES['images-tags'] = (
    "CREATE TABLE `tags` ("
    "  `tag_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `url` char(60) NOT NULL,"
    "  `tag` char(50) NOT NULL,"
    "  PRIMARY KEY (`tag_no`)"
    ") ENGINE=InnoDB")

def create_table(cursor):
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except MySQL.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

create_table(cursor)

add_user = ("INSERT INTO  users "
            "(username, lasttweet) "
            "VALUES (%s, %s)")

add_image = ("INSERT INTO  images "
            "(username, url) "
            "VALUES (%s, %s)")

add_tag = ("INSERT INTO  tags "
            "(url, tag) "
            "VALUES (%s, %s)")

userquery = ("SELECT lasttweet FROM users "
             "WHERE username = %s")

imagequery = ("SELECT url FROM images "
             "WHERE username = %s")

tagquery = ("SELECT tag FROM tags "
           "WHERE url = %s")

tagqueryneg = ("SELECT url FROM tags "
           "WHERE tag = %s")

imagequeryneg = ("SELECT username FROM images "
             "WHERE url = %s")

tagqueryall = ("SELECT tag FROM tags ")

cursor.close()

def postnewdata(username, lasttweet, imgurllist, taglist):
    """Used to create a new user."""
    cursor = db.cursor()
    cursor.execute(add_user, (username, lasttweet))

    for i, image in enumerate(imgurllist):
        cursor.execute(add_image, (username, image))
        for tag in taglist[i]:
            cursor.execute(add_tag, (image, tag))

    db.commit()
    cursor.close()

def checkdata(username):
    """Gets the most recent tweet found by the database for given user."""
    # If user is not in database, return -1.
    cursor = db.cursor()

    cursor.execute(userquery, (username, ))

    lasttweet = -1

    urllist = []

    taglist = []

    for num in cursor:
        lasttweet = int(num[0])

    cursor.execute(imagequery, (username, ))

    for image in cursor:
        urllist.append(image[0])

    for image in urllist:
        cursor.execute(tagquery, (image, ))
        temptaglist = []
        for tag in cursor:
            temptaglist.append(tag[0])
        taglist.append(temptaglist)

    cursor.close()

    return(lasttweet, urllist, taglist)

def updatedata(username, lasttweet, imgurllist, taglist):
    """Used to update user data in db."""
    cursor = db.cursor()
    for i, image in enumerate(imgurllist):
        cursor.execute(add_image, (username, image))
        for tag in taglist[i]:
            cursor.execute(add_tag, (image, tag))
    db.commit()
    cursor.close()

def findstring(string):
    """Used to return data about a certain tag within the database."""
    cursor = db.cursor()

    cursor.execute(tagqueryneg, (string, ))

    urlarray = []

    for url in cursor:
        urlarray.append(url[0])

    returnarray = []

    for url in urlarray:
        cursor.execute(imagequeryneg, (url, ))
        for username in cursor:
            returnarray.append(username[0])

    cursor.close()

    return returnarray

def findalltags():

    cursor = db.cursor()

    cursor.execute(tagqueryall)

    returndic = {}

    for tag in cursor:
        if tag[0] not in returndic:
            returndic[tag[0]] = 1
        else:
            returndic[tag[0]] = returndic[tag[0]] + 1

    cursor.close()

    return returndic

def finishup():
    db.close()

    return 0
