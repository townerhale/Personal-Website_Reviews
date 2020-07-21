import sqlite3
from sqlite3 import Error


def sql_connect(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


# SQL_Create - Create the tables for the SQL database, only needs to be ran once
def sql_create(conn):
    cur = conn.cursor()

    with open('SQL.sql') as fp:
        cur.executescript(fp.read())


def sql_test(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def sql_load():
    database = "database.db"

    conn = sql_connect(database)
    # with conn:
        # SQL_Create(conn)
        # sql_test(conn)

    return conn
