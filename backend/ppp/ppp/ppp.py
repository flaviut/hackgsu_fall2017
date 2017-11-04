import os
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'ppp.db'),
    SECRET_KEY='dev_key',
    USERNAME='pottypatrol',
    PASSWORD='superportable'
))
app.config.from_envvar('PPP_SETTINGS', silent=true)

def connect_db():
    r = sqlite3.connect(app.config['DATABASE'])
    r.row_factory = sqlite3.Row
    return r

