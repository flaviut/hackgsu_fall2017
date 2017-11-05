from ppp import app

import json
import sqlite3 as sql
from flask import request

# json thing
myToilets = {"toilets": [{"id": "1", "toiletId": "1", "ts": "2017-11-01T11:40:20+00:00", "action": "closed"},
                         {"id": "2", "toiletId": "2", "ts": "2017-11-01T10:35:22+00:00", "action": "closed"},
                         {"id": "3", "toiletId": "3", "ts": "2017-11-01T07:41:16+00:00", "action": "open"},
                         {"id": "4", "toiletId": "4", "ts": "2017-11-01T03:31:51+00:00", "action": "open"},
                         {"id": "5", "toiletId": "5", "ts": "2017-11-01T11:02:45+00:00", "action": "closed"},
                         {"id": "6", "toiletId": "6", "ts": "2017-11-02T15:04:36+00:00", "action": "open"},
                         {"id": "7", "toiletId": "7", "ts": "2017-11-02T17:06:36+00:00", "action": "closed"}]}


@app.route('/database')
def toilet_info():
    con = sql.connect('test.db')
    with con:
        c = con.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Toilets(id INTEGER PRIMARY KEY,toiletId INTEGER, ts TEXT, action TEXT)")
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
        c.execute('SELECT max(id) FROM Toilets')
        num = c.fetchall()
        num2 = num[0][0]
        if (num2 < 7):
            for num in myToilets['toilets']:
                c.execute('INSERT INTO Toilets (ts, action) VALUES (?,?)', (num['ts'], num['action']))
    return "Data inserted"


@app.route('/post', methods=['POST'])
def post():
    con = sql.connect('test.db')
    with con:
        cur = con.cursor()
        values = (
            request.values.get('toiletId', type=int),
            request.values.get('ts', type=str),
            request.values.get('action', type=str))
        cur.execute('INSERT INTO Toilets (toiletId, ts, action) VALUES (?,?,?)', values)
    return json.dumps(values)


@app.route('/load')
def index():
    con = sql.connect('test.db')
    con.row_factory = sql.Row
    c = con.cursor()
    c.execute("""
        SELECT * FROM Toilets
        WHERE datetime('now', '-10 days') < datetime(ts)
        ORDER BY ts""")
    rows = c.fetchall()
    results = []
    for row in rows:
        results.append(tuple(row))
    db_size = c.execute('SELECT max(id) FROM Toilets').fetchall()[0][0]

    if len(results) < 8 and db_size > 8:
        rows = c.execute("""
            SELECT * FROM Toilets T1 WHERE T1.id IN (
                SELECT T2.id FROM Toilets T2
                WHERE T2.toiletId = T1.toiletId
                ORDER BY T2.ts
                LIMIT 8
            )
            ORDER BY T1.toiletId""").fetchall()
        for row in rows:
            results.append(tuple(row))
    return json.dumps(results)


@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
