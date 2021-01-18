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
def dbadd() -> bool:
    """Add data to the database."""
    data = json.loads(request.get_json())
    with sqlite3.connect("datastore/userinfo.db") as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("INSERT INTO userinfo (username, email) VALUES (?, ?)",
                       (data["name"], data["email"]))
        conn.commit()
        return "success"
# TODO: Add failure case


@APP.route("/dev/db/<user>", methods=["GET"])
@AUTH.login_required
def getuser(user: str) -> dict:
    """Retrieve user information from the database."""
    with sqlite3.connect("datastore/userinfo.db") as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("SELECT username, email FROM userinfo WHERE username LIKE "
                       + "\"" + user + "\"")
        retdata: dict = {"result": [{"name": row[0], "email": row[1]}
                              for row in tmpcur if row is not None]}
    return json.dumps(retdata)


@APP.route("/dev/db", methods=["GET"])
@AUTH.login_required
def dbdump() -> dict:
    """Retrieve full database contents."""
    with sqlite3.connect("datastore/userinfo.db") as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("SELECT username, email FROM userinfo")
        retdata = {"result": [{"name": row[0], "email": row[1]}
                              for row in tmpcur if row is not None]}
    return json.dumps(retdata)


@APP.route("/dev/db/<user>", methods=["DELETE"])
@AUTH.login_required
def deluser(user: str) -> bool:
    """Delete a single user from the user database."""
    with sqlite3.connect("datastore/userinfo.db") as conn:
        tmpcur = conn.cursor()
        tmpcur.execute(
            "DELETE FROM userinfo WHERE username LIKE " + "\"" + user + "\"")
        return "success"
# TODO: Add failure case


@APP.route("/dev/db/<user>", methods=["PATCH"])
@AUTH.login_required
def updateuser(user: str) -> bool:
    """Update a given user's e-mail address."""
    data: dict = json.loads(request.json)
    with sqlite3.connect("datastore/userinfo.db") as conn:
        tmpcur = conn.cursor()
        tmpcur.execute("UPDATE userinfo SET email = " + "\"" +
                       data["email"] + "\" WHERE username LIKE " + "\"" + user + "\"")
        return "success"
# TODO: Add failure case


if __name__ == "__main__":
    ENABLE_SSL: bool = False
    if ENABLE_SSL:
        APP.run(ssl_context="adhoc")
    else:
        APP.run(debug=True)
