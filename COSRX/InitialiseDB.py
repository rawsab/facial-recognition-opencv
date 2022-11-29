import mysql.connector

from datetime import datetime
    

# must create new user with all privs before using
# update the user and password to your choice
def makeConnection():
    db = mysql.connector.connect(
        host='localhost',
        user='hudson',
        password='password'
    )
    return db

def getDateTime():
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')


def initialiseDBs():
    db = makeConnection()
    cursor = db.cursor()

    cursor.execute('CREATE DATABASE AuthenticatedUsers;')
    cursor.execute('USE AuthenticatedUsers;')
    cursor.execute('CREATE TABLE users(name VARCHAR(255), filePath VARCHAR(255);')
    cursor.execute('CREATE TABLE dailyLogs(name VARCHAR(255), time DATETIME);')
    cursor.execute('COMMIT')
    
    cursor.execute('USE mysql;')
    
    cursor.execute('CREATE DATABASE UnauthorisedUsers;')
    cursor.execute('USE UnauthorisedUsers;')
    cursor.execute('CREATE TABLE dailyLogs(filepath VARCHAR(255), time DATETIME);')
    cursor.execute('COMMIT')
    
    
    