#Copyright 2018 Nathan Wiebe nwiebe@bu.edu
#EC 601 Mini Project 1 MySQL module

import sys
try:
    import _mysql as MySQL
except ModuleNotFoundError:
    print("Please run $ pip install mysqlclient-python .")
    sys.exit(1)

# Add host= user= and passwd= parameters if necessary.
try:
    db = MySQL.connect(db="miniprojectdb")
except:
    print("Either the MySQL server is not running or the database is not created.")
    sys.exit(1)



