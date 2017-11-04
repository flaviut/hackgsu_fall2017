from ppp import app

import json
import sqlite3 as sql

#studnet object with parsed JSON
student = {"101":{"class":'V', "Name":'Rohit',  "Roll_no":7},
           "102":{"class":'V', "Name":'David',  "Roll_no":8},
           "103":{"class":'V', "Name":'Samiya', "Roll_no":12}}

#json thing
myToilets = {"toilets":[{"id": "1","timestamp": "...","action": "closed"},
    				  {"id": "2","timestamp": "...","action": "closed"},
    	  			  {"id": "3","timestamp": "...","action": "open"},
					  {"id": "4","timestamp": "...","action": "open"},
					  {"id": "5","timestamp": "...","action": "closed"},
					  {"id": "6","timestamp": "...","action": "open"},
    	  			  {"id": "7","timestamp": "...","action": "closed"}]}

		# cur.execute("INSERT INTO MyTable1 VALUES(1, 'EntryOne')")
		# cur.execute("INSERT INTO MyTable1 VALUES(2, 'EntryTwo')")
		# cur.execute("INSERT INTO MyTable1 VALUES(3, 'EntryThree')")
@app.route('/what')
def wha_t():
	x = 0
	for num in myToilets['toilets']:
		x += 1
	return str(x)
@app.route('/toilets')
def toilet_info():
	con = sql.connect('test.db')
	with con:
		c = con.cursor()
		# c.executemany("INSERT INTO Toilets(id, timestamp, action)"
		# 			  "VALUES (:id, :timestamp, :action)", json.loads(toilets)['toilets'])
		# c.executemany('INSERT INTO data (id, timestamp, action) '
        #          	  'VALUES (:id, :timestamp, :action)', json.loads(myToilets)['toilets'])
		for num in myToilets['toilets']:
			c.execute('INSERT INTO Toilets (id, timestamp, action, toiletId) VALUES (?,?,?,?)', (num['id'], num['timestamp'], num['action'], num['toiletId']))
	return "Success"
@app.route('/database')
def make_db():
	con = sql.connect('test.db')
	with con:
		cur = con.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS Toilets(id INT, timestamp TEXT, action TEXT)")
	return "Success"
@app.route('/json')
def index():
	return json.dumps(student)
