import os
import sqlite3
from datetime import date


def get_connection(db_name):
    conn = sqlite3.connect(db_name)
    return conn.cursor(), conn


def create_table(connection):
    connection.execute('''CREATE TABLE IF NOT EXISTS
                                 problems (collection TEXT,
                                           seed INT,
                                           success BOOL,
                                           date date,
                                           UNIQUE(collection, seed)
                                           );''')


path = os.path.dirname(__file__)
db = os.path.join(path, 'tsumegos.db')
cursor, connection = get_connection(db)
create_table(connection)


def solved_daily_problem():
    today = date.today()
    sql = f'SELECT COUNT(seed) FROM problems WHERE date={today}'
    connection.execute(sql)

    rows = cursor.fetchone()

    if rows is None:
        return False
    else:
        rows = rows[0]

    if rows < 4:
        return False
    return True


def get_solved_problems(collection):
    sql = f"""SELECT collection, seed
              FROM problems WHERE
              success=True AND collection='{collection}'"""
    indices = []
    for collection, i in connection.execute(sql):
        indices.append(i)

    return indices


def insert_problem(collection, seed, success):
    today = date.today()
    sql = f'''INSERT INTO problems VALUES
              ('{collection}', {seed}, {success}, {today})'''
    try:
        connection.execute(sql)
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
