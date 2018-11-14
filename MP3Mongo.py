#Copyright 2018 Nathan Wiebe nwiebe@bu.edu
#EC 601 Mini Project 1 Google Vision Module

from pymongo import MongoClient

# Establish connection with default Mongo Client.
client = MongoClient()

# Access MP3 database.
db = client.pymongo_test