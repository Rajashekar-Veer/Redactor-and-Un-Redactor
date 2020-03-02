import sqlite3
import tempfile
import PyPDF2 as pd
import numpy as np
import pandas as p
import re
from urllib import request

temp = tempfile.TemporaryFile(suffix='temp.pdf')
def fetchIncidents(url):
    # this function is used to read a file and store the content in temp file
    response = request.urlopen(url)
    pdf = response.read()
    temp.write(pdf)
    return temp

def extractIncidents():
    #this function is used to extract content and store each record in a list of list.
    list = []
    dataStr = ''
    pdfReader = pd.pdf.PdfFileReader(temp)
    data = pdfReader
    pageCount = pdfReader.getNumPages()
    for i in range(0, pageCount):
        data = pdfReader.getPage(i).extractText()
        dataStr += data
    data = re.sub('NORMAN POLICE DEPARTMENT\n','',dataStr)
    data = re.sub('Daily Incident Summary \(Public\)','',data)
    data = re.sub(' \n', ' ', data)
    data = re.split(r'\s+(?=\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{1,2})', data)
    for i in data:
        data = i.split('\n')
        if len(data) <= 4:
            data.insert(3,'NA')
        list.append(data)
    data = list[1:-1]
    return data

def createdb():
    #this function creates the db and also creates the table incidents
    try:
        database = 'policeDept.db'
        db = sqlite3.connect(database)
        point = db.cursor()
        dropScript = 'DROP TABLE IF EXISTS incidents;'
        createScript = 'CREATE TABLE IF NOT EXISTS incidents (DataTime TEXT, incidentNumber TEXT, location TEXT, Nature TEXT, incidentORI TEXT);'
        point.execute(dropScript)
        point.execute(createScript)
        db.commit()
        return database
    except sqlite3.Error as error:
        print(error)


def dbInsert(db, incidents):
    #this function inserts the extracted data into incidents table
    db = sqlite3.connect(db)
    point = db.cursor()
    insertQuery = 'INSERT INTO incidents VALUES (?, ?, ?, ?, ?);'
    for i in range(len(incidents)):
        point.execute(insertQuery, incidents[i])
        db.commit()

def dbStatus(db):
    #this function is used to display the count of nature from the incidents table
    db = sqlite3.connect(db)
    point = db.cursor()
    point.execute('SELECT nature||"|"||count(*) as nature FROM incidents group by nature order by nature;')
    myResult = point.fetchall()
    for row in myResult:
        print(row[0])
    return myResult