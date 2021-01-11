import sqlite3

conn = sqlite3.connect('datastore/userinfo.db')

conn.execute("CREATE TABLE userinfo (username CHAR(20) PRIMARY KEY NOT NULL, email CHAR(40) NOT NULL)")

conn.close
