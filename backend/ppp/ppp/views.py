from ppp import app

import json
import sqlite3 as sql

#json thing
myToilets = {"toilets":[{"id": "1", "toiletId": "1", "timestamp": "2017-11-01T11:40:20+00:00", "action": "closed"},
                      {"id": "2", "toiletId": "2", "timestamp": "2017-11-01T10:35:22+00:00", "action": "closed"},
                        {"id": "3", "toiletId": "3", "timestamp": "2017-11-01T07:41:16+00:00", "action": "open"},
                      {"id": "4", "toiletId": "4", "timestamp": "2017-11-01T03:31:51+00:00", "action": "open"},
                      {"id": "5", "toiletId": "5", "timestamp": "2017-11-01T11:02:45+00:00", "action": "closed"},
                      {"id": "6", "toiletId": "6", "timestamp": "2017-11-02T15:04:36+00:00", "action": "open"},
                        {"id": "7", "toiletId": "7", "timestamp": "2017-11-02T17:06:36+00:00", "action": "closed"}]}

@app.route('/database')
def toilet_info():
    con = sql.connect('test.db')
    with con:
        c = con.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Toilets(id INTEGER PRIMARY KEY,toiletId INTEGER, timestamp TEXT, action TEXT)")
        # c.execute('DROP TABLE IF EXISTS Toilets')
    return "Success"
@app.route('/showdbcolumn')
def show_db_column():
    con = sql.connect('test.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('SELECT id FROM Toilets')
    rows = cur.fetchall()
    list = []
    for row in rows:
        list.append(tuple(row))
    return json.dumps(list)
@app.route('/addinfo')
def add_info():
    con = sql.connect('test.db')
    with con:
        c = con.cursor()
        c.execute('SELECT max(id) from Toilets')
        num = c.fetchall()
        num2 = num[0][0]
        if (num2 < 7):
            for num in myToilets['toilets']:
                c.execute('INSERT INTO Toilets (timestamp, action) VALUES (?,?)', (num['timestamp'], num['action']))
    return "Data inserted"
@app.route('/load')
def index():
   return json.dumps(myToilets)
