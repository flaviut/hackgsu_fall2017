from app import app

import json
import sqlite3 as sql

#studnet object with parsed JSON
student = {"101":{"class":'V', "Name":'Rohit',  "Roll_no":7},
           "102":{"class":'V', "Name":'David',  "Roll_no":8},
           "103":{"class":'V', "Name":'Samiya', "Roll_no":12}}

#json thing
toilets = {{"id": 1,"timestamp": "...","action": "open"},
		   {"id": 2,"timestamp": "...","action": "closed"},
		   {"id": 3,"timestamp": "...","action": "closed"},
		   {"id": 4,"timestamp": "...","action": "open"}}

@app.route('/toilets')
def toilet_info():

	return "zz"
@app.route('/database')
def make_db():
	con = sql.connect('test.db')
	with con:
		cur = con.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS MyTable1(FieldOne INT, FieldTwo TEXT)")
		cur.execute("INSERT INTO MyTable1 VALUES(1, 'EntryOne')")
		cur.execute("INSERT INTO MyTable1 VALUES(2, 'EntryTwo')")
		cur.execute("INSERT INTO MyTable1 VALUES(3, 'EntryThree')")
	return "Success"
@app.route('/json')
def index():
    #returns JSON
	return json.dumps(student)
