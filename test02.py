"""First RestAPI"""


# Need to do this next:
# https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

import sqlite3
import json
from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

APP = Flask(__name__)
auth = HTTPBasicAuth()


users = {
    "ben": generate_password_hash("ben"),
    "rod": generate_password_hash("rod")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@APP.route('/')
def home():
    """ Client Script """
    return render_template("full-cli-v1.html")


@APP.route('/dev/db', methods=['POST'])
@auth.login_required
def dbadd():
    """ Database Add"""
    data = json.loads(request.get_json())
    with sqlite3.connect('datastore/userinfo.db') as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("INSERT INTO userinfo (username, email) VALUES (?, ?)",
                       (data['name'], data['email']))
        conn.commit()
        return "success"


@APP.route('/dev/db/<user>', methods=['GET'])
@auth.login_required
def getuser(user):
    """ Return single user info """
    with sqlite3.connect('datastore/userinfo.db') as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("SELECT username, email FROM userinfo WHERE username LIKE "
                       + "\"" + user + "\"")
        retdata = {'result': [{'name': row[0], 'email': row[1]}
                              for row in tmpcur if row is not None]}
        return json.dumps(retdata)


@APP.route('/dev/db', methods=['GET'])
@auth.login_required
def dbdump():
    """ Return DB contents"""
    with sqlite3.connect('datastore/userinfo.db') as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("SELECT username, email FROM userinfo")
        retdata = {'result': [{'name': row[0], 'email': row[1]}
                              for row in tmpcur if row is not None]}
        return json.dumps(retdata)


@APP.route('/dev/db/<user>', methods=['DELETE'])
@auth.login_required
def deluser(user):
    """ Delete single user """
    with sqlite3.connect('datastore/userinfo.db') as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("DELETE FROM userinfo WHERE username LIKE " + "\"" + user + "\"")
        return "success"


@APP.route('/dev/db/<user>', methods=['PATCH'])
@auth.login_required
def updateuser(user):
    """ Update user email """
    data = json.loads(request.json)
    with sqlite3.connect('datastore/userinfo.db') as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("UPDATE userinfo SET email = " + "\"" +
                       data['email'] + "\" WHERE username LIKE " + "\"" + user + "\"")
        return "success"


if __name__ == "__main__":
    APP.run(debug=True)#, ssl_context='adhoc')
    #APP.run(ssl_context='adhoc')
