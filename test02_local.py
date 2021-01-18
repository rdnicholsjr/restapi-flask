"""Learning proect for a RESTful API."""

# TODO: https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

import sqlite3
import json
from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

APP = Flask(__name__)
CORS(APP)
AUTH = HTTPBasicAuth()


USERS: dict = {
    "ben": generate_password_hash("ben"),
    "rod": generate_password_hash("rod")
}
SITE_INDEX: str = "test-page1.html"


@AUTH.verify_password
def verify_password(username: str, password: str) -> dict:
    """Check if the supplied username and passowrd multiplex matches the stored password."""
    results: dict = {"username": username, "authorized": False}
    results["authorized"] = bool(
        username in USERS and check_password_hash(USERS.get(username), password))
    return results


@APP.route("/")
@AUTH.login_required
def home():
    """Index page for the website."""
    return render_template(SITE_INDEX)


@APP.route("/dev/db", methods=["POST"])
@AUTH.login_required
def dbadd():
    """Add data to the database."""
    data = json.loads(request.get_json())
    with sqlite3.connect("datastore/userinfo.db") as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("INSERT INTO userinfo (username, email) VALUES (?, ?)",
                       (data["name"], data["email"]))
        conn.commit()
        return "success"


@APP.route("/dev/db/<user>", methods=["GET"])
@AUTH.login_required
def getuser(user):
    """Retrieve user information from the database."""
    with sqlite3.connect("datastore/userinfo.db") as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("SELECT username, email FROM userinfo WHERE username LIKE "
                       + "\"" + user + "\"")
        retdata = {"result": [{"name": row[0], "email": row[1]}
                              for row in tmpcur if row is not None]}
        return json.dumps(retdata)


@APP.route("/dev/db", methods=["GET"])
@AUTH.login_required
def dbdump():
    """Retrieve full database contents."""
    with sqlite3.connect("datastore/userinfo.db") as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("SELECT username, email FROM userinfo")
        retdata = {"result": [{"name": row[0], "email": row[1]}
                              for row in tmpcur if row is not None]}
        return json.dumps(retdata)


@APP.route("/dev/db/<user>", methods=["DELETE"])
@AUTH.login_required
def deluser(user):
    """Delete a single user from the user database."""
    with sqlite3.connect("datastore/userinfo.db") as conn:
        tmpcur = conn.cursor()
        tmpcur.execute(
            "DELETE FROM userinfo WHERE username LIKE " + "\"" + user + "\"")
        return "success"


@APP.route("/dev/db/<user>", methods=["PATCH"])
@AUTH.login_required
def updateuser(user):
    """Update a given user's e-mail address."""
    data = json.loads(request.json)
    with sqlite3.connect("datastore/userinfo.db") as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("UPDATE userinfo SET email = " + "\"" +
                       data["email"] + "\" WHERE username LIKE " + "\"" + user + "\"")
        return "success"


if __name__ == "__main__":
    APP.run(debug=True)  # , ssl_context="adhoc")
    # APP.run(ssl_context="adhoc")
