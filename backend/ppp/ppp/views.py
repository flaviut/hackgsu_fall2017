from ppp import app

import json
import sqlite3 as sql

s = "test"

#studnet object with parsed JSON
student = {"101":{"class":'V', "Name":'Rohit',  "Roll_no":7},
           "102":{"class":'V', "Name":'David',  "Roll_no":8},
           "103":{"class":'V', "Name":'Samiya', "Roll_no":12}}

#json thing
myToilets = {"toilets":[{"id": "1", "toiletId": "1", "timestamp": "...", "action": "closed"},
                      {"id": "2", "toiletId": "2", "timestamp": "...", "action": "closed"},
                        {"id": "3", "toiletId": "3", "timestamp": "...", "action": "open"},
                      {"id": "4", "toiletId": "4", "timestamp": "...", "action": "open"},
                      {"id": "5", "toiletId": "5", "timestamp": "...", "action": "closed"},
                      {"id": "6", "toiletId": "6", "timestamp": "...", "action": "open"},
                        {"id": "7", "toiletId": "7", "timestamp": "...", "action": "closed"}]}
@app.route('/what')
def wha_t():
    x = 0
    for num in myToilets['toilets']:
        x += 1
    return str(x)
@app.route('/database')
def toilet_info():
    con = sql.connect('test.db')
    with con:
        c = con.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Toilets(id INTEGER PRIMARY KEY,toiletId INT, timestamp TEXT, action TEXT)")
        for num in myToilets['toilets']:
            c.execute('INSERT INTO Toilets (timestamp, action) VALUES (?,?)', (num['timestamp'], num['action']))
    return "Success"
@app.route('/showdbcolumn')
def show_db_column():
	con = sql.connect('test.db')
	con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute('SELECT action FROM Toilets')
	rows = cur.fetchall()
	list = []
	for row in rows:
		list.append(tuple(row))
	return json.dumps(list)
@app.route('/json')
def index():
   return json.dumps(student)
