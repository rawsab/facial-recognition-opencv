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


def newAuthUser(name, filepath):
    db = makeConnection()
    cursor = db.cursor()
    dateTime = getDateTime()
    cursor.execute('USE AuthenticatedUsers')
    cursor.execute('INSERT INTO users(name, filepath) values(%s,%s)', (name,filepath))
    cursor.execute('COMMIT')


def removeAuthUser(name):
    db = makeConnection()
    cursor = db.cursor()
    dateTime = getDateTime()
    cursor.execute('USE AuthenticatedUsers')
    cursor.execute("DELETE FROM users WHERE name='" + name +"'")
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
    cursor.execute('USE UnauthorisedUsers')
    cursor.execute('INSERT INTO dailyLogs(filepath, time) values(%s,%s)', (filePath,dateTime))
    cursor.execute('COMMIT')


def printLogs(table):
    mydb = makeConnection()
    mycursor = mydb.cursor()
    mycursor.execute("USE AuthenticatedUsers")
    print('SELECT *FROM ' + table)
    mycursor.execute('SELECT *FROM ' + table)
    
    res = mycursor.fetchall()
    for x in res:
        print(x)


def getLogs(table):
    mydb = makeConnection()
    mycursor = mydb.cursor()
    mycursor.execute("USE AuthenticatedUsers")
    print('SELECT *FROM ' + table)
    mycursor.execute('SELECT *FROM ' + table)
    
    res = mycursor.fetchall()
    li = []
    for x in res:
        li.append(x)
    return li


def getUnauthLogs():
    mydb = makeConnection()
    mycursor = mydb.cursor()
    mycursor.execute("USE UnauthorisedUsers")
    mycursor.execute("SELECT *FROM dailyLogs;")
    res = mycursor.fetchall()
    li = []
    for x in res:
        li.append(x)
    return li    