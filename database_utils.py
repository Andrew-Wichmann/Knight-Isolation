import sqlite3
from sqlite3 import Error
from os.path import realpath

DEFAULT_TABLE = "CREATE TABLE {} (player_1 varchar(50) NOT NULL, player_2 varchar(50) NOT NULL, player_1_wins integer NOT NULL, player_2_wins integer NOT NULL)"

def create_db(filepath='./sqlite'):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(realpath(filepath))
    except Error as e:
        print(e)
    finally:
        conn.close()

def get_connection(dbfile='./sqlite'):
    try:
        return sqlite3.connect(realpath(dbfile))
    except Error as e:
        print(e)

def get_cursor(dbfile='./sqlite'):
    try:
        return sqlite3.connect(realpath(dbfile)).cursor()
    except Error as e:
        print(e)

def create_table(dbfile='./sqlite', table_name='match_history', statement=DEFAULT_TABLE):
    conn = get_connection(dbfile)
    try:
        cursor = conn.cursor()
        cursor.execute(statement.format(table_name))
    except Error as e:
        print(e)

def drop_table(dbfile='./sqlite', table_name='match_history'):
    conn = get_connection(dbfile)
    try:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE {}".format(table_name))
    except Error as e:
        print(e)

def insert_into_table(values=('minimax', 'greedy', 0, 0), dbfile='./sqlite', table_name='match_history'):

    STATEMENT = "INSERT INTO {}(player_1, player_2, player_1_wins, player_2_wins) VALUES{};".format(table_name, values)

    with get_connection(dbfile) as conn:
        c = conn.cursor()
        c.execute(STATEMENT)

def update_table(p1_wins, p2_wins, p1, p2):

    STATEMENT = "UPDATE match_history SET player_1_wins = {}, player_2_wins = {} WHERE player_1 = '{}' AND player_2 = '{}';".format(p1_wins, p2_wins, p1, p2)
    with get_connection() as conn:
        c = conn.cursor()
        c.execute(STATEMENT)

def select_match(p1, p2):

    STATEMENT = "SELECT * FROM match_history WHERE player_1 = '{}' AND player_2 = '{}';".format(p1, p2)

    with get_connection() as conn:
        c = conn.cursor()
        c.execute(STATEMENT)
        return c.fetchall()

def select_all():

    STATEMENT = 'SELECT * FROM match_history'

    with get_connection() as conn:
        c = conn.cursor()
        c.execute(STATEMENT)
        return c.fetchall()
