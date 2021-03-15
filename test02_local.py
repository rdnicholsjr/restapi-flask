"""First RestAPI"""

# Need to do this next:
# https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

import sqlite3
import json
from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

APP = Flask(__name__)
CORS(APP)
AUTH = HTTPBasicAuth()
ENABLE_SSL: bool = False
SITE_INDEX: str = 'test-page1.html'


users = {
    "ben": generate_password_hash("ben"),
    "rod": generate_password_hash("rod")
}

def shut_up_pylint(username: str) -> str :
    return username


@AUTH.verify_password
def verify_password(username: str, password: str) -> str:
    """ Return string: username if hash maches on provided password and userdb hash """
    if username in users and \
            check_password_hash(users.get(username), password):
        return shut_up_pylint(username)


@APP.route('/')
@AUTH.login_required
def home():
    """ Client Script """
    return render_template(SITE_INDEX)


@APP.route('/dev/db', methods=['POST'])
@AUTH.login_required
def dbadd() -> dict:
    """ Database Add"""
    with sqlite3.connect('datastore/userinfo.db') as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("INSERT INTO userinfo (username, email) VALUES (?, ?)",
                       (request.json['name'], request.json['email']))
        conn.commit()
        return json.dumps({'result': True})


@APP.route('/dev/db/<user>', methods=['GET'])
@AUTH.login_required
def getuser(user: str) -> str:
    """ Return single user info """
    with sqlite3.connect('datastore/userinfo.db') as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("SELECT username, email FROM userinfo WHERE username LIKE "
                       + "\"" + user + "\"")
        retdata = {'result': [{'name': row[0], 'email': row[1]}
                              for row in tmpcur if row is not None]}
        return json.dumps(retdata)


@APP.route('/dev/db', methods=['GET'])
@AUTH.login_required
def dbdump() -> str:
    """ Return DB contents"""
    with sqlite3.connect('datastore/userinfo.db') as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("SELECT username, email FROM userinfo")
        retdata = {'result': [{'name': row[0], 'email': row[1]}
                              for row in tmpcur if row is not None]}
        return json.dumps(retdata)


@APP.route('/dev/db/<user>', methods=['DELETE'])
@AUTH.login_required
def deluser(user: str)-> dict:
    """ Delete single user """
    with sqlite3.connect('datastore/userinfo.db') as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("DELETE FROM userinfo WHERE username LIKE " + "\"" + user + "\"")
        return json.dumps({'result': True})


@APP.route('/dev/db/<user>', methods=['PATCH'])
@AUTH.login_required
def updateuser(user: str) -> dict:
    """ Update user email """
    with sqlite3.connect('datastore/userinfo.db') as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("UPDATE userinfo SET email = " + "\"" +
                       request.json + "\" WHERE username LIKE " + "\"" + user + "\"")
        return json.dumps({'result': True})


if __name__ == "__main__":
    if ENABLE_SSL:
        APP.run(ssl_context='adhoc')
    else:
        APP.run(debug=True)
