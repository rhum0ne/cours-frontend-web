import sqlite3
from pathlib import Path


def reset_database():
    path = "database.db"
    
    Path(path).touch(exist_ok=True) # create the file if it doesn't exist
    
    db_connection = sqlite3.connect(path)
    cur = db_connection.cursor()

    # drop the tables if they exist
    cur.execute("drop table if exists QuestionAnswer")
    cur.execute("drop table if exists Question")

    # create the tables
    cur.execute(
        "create table Question (id integer primary key autoincrement, title text, position integer)")
    cur.execute(
        "create table QuestionAnswer (id integer primary key autoincrement, question integer, text text, is_correct boolean)")

def get_connection() -> sqlite3.Connection:
    return create_connection()

def create_connection() -> sqlite3.Connection:
    path = "database.db"
    db_connection = sqlite3.connect(path)

    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None
    
    return db_connection