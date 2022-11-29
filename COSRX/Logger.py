import mysql.connector

from datetime import datetime


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

def searchByDay(str):
    print(getDateTime())

def removeAuthUser(name):
    db = makeConnection()
    cursor = db.cursor()
    dateTime = getDateTime()

    cursor.execute('USE AuthenticatedUsers')
    cursor.execute("DELETE FROM users WHERE name='" + name +"'")
    cursor.execute('COMMIT')

    
def newAuthUser(name, filepath):
    db = makeConnection()
    cursor = db.cursor()
    dateTime = getDateTime()

    cursor.execute('USE AuthenticatedUsers')
    cursor.execute('INSERT INTO users(name, filepath) values(%s,%s)', (name,filepath))
    cursor.execute('COMMIT')

def logAuthUser(name):
    db = makeConnection()
    cursor = db.cursor()
    dateTime = getDateTime()

    cursor.execute('USE AuthenticatedUsers')
    cursor.execute('INSERT INTO dailyLogs(name, time) values(%s,%s)', (name,dateTime))
    cursor.execute('COMMIT')


def logUnauthUser(filePath):
    db = makeConnection()
    cursor = db.cursor()
    dateTime = getDateTime()
    cursor.execute('USE UnauthorrisedUsers')
    cursor.execute('INSERT INTO dailyLogs(filepath, time) values(%s,%s)', (filepath,dateTime))
    cursor.execute('COMMIT')

def printLogs(table):
    db = makeConnection()
    cursor = mydb.cursor()
    cursor.execute("USE AuthenticatedUsers")
    print('SELECT *FROM ' + table)
    cursor.execute('SELECT *FROM ' + table)
    
    res = cursor.fetchall()
    for x in res:
        print(x)


def printUserLogs(name):
    db = makeConnection()
    cursor = db.cursor()
    cursor.execute("USE userlogs")
    cursor.execute("SELECT *FROM logs;")
    res = cursor.fetchall()
    for x in res:
        if (x[1] == name):
            print(x)


# returns the filepath to all images taken of unauthorised users between the given dates
def getImagePaths(start, end):
    db = makeConnection()
    cursor = db.cursor()
    cursor.execute('USE UnauthorisedUsers')
    cursor.execute("SELECT *FROM TABLENAME WHERE time >= '%s' time <= '%s';", (start,end))
    res = cursor.fetchall()
    for x in res:
        print(x)

