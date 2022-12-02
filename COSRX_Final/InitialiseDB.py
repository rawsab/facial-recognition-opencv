import mysql.connector

# 1) Download mysql and create a new user with all priveleges before using
# 2) Update the user and password to your choice
# 3) You may have to call "sudo systemctl enable mariadb.service" to keep the DB alive
def makeConnection():
    db = mysql.connector.connect(
        host='localhost',
        user='YOUR_USERNAME',
        password='YOUR_PASSWORD'
    )
    return db

# initialise database to log users
def initialiseDBs():
    db = makeConnection()
    cursor = db.cursor()

    cursor.execute('CREATE DATABASE AuthenticatedUsers;')
    cursor.execute('USE AuthenticatedUsers;')
    cursor.execute('CREATE TABLE users(name VARCHAR(255), filePath VARCHAR(255);')
    cursor.execute('CREATE TABLE dailyLogs(name VARCHAR(255), time DATETIME);')
    cursor.execute('COMMIT')
    
    cursor.execute('USE mysql;')
    
    cursor.execute('CREATE DATABASE UnauthenticatedUsers;')
    cursor.execute('USE UnauthenticatedUsers;')
    cursor.execute('CREATE TABLE dailyLogs(filepath VARCHAR(255), time DATETIME);')
    cursor.execute('COMMIT')
    
    
    