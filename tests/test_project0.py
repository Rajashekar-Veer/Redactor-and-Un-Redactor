import pytest
import sqlite3
from project0 import project0


url = 'http://normanpd.normanok.gov/filebrowser_download/657/2020-02-27%20Daily%20Incident%20Summary.pdf'

def test_fetchIncidents():
    assert project0.fetchIncidents(url) is not None

def test_extractIncidents():
    data = project0.extractIncidents()
    for i in data:
        assert len(i) == 5

def test_createdb():
    databaseName = project0.createdb()
    assert databaseName == 'policeDept.db'

def test_dbInsert():
    db = project0.createdb()
    incidents = project0.extractIncidents()
    project0.dbInsert(db, incidents)
    dbase = sqlite3.connect(db)
    point = dbase.cursor()
    point.execute('select count(*) from incidents;')
    count = point.fetchone()
    assert count[0] == len(incidents)

def test_dbStatus():
    db = project0.createdb()
    incidents = project0.extractIncidents()
    project0.dbInsert(db, incidents)
    records = project0.dbStatus(db)
    assert records is not None

