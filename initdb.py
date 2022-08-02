"""
Provides a method to initalize a local sqlite database
"""
import sqlite3


def initalize_db():
    """ set local database to settings per the schema """
    conn = None
    try:
        conn = sqlite3.connect("database.db")

        with open("myschema.sql", "r", encoding="utf8") as sql_file:
            sql_script = sql_file.read()

        database = sqlite3.connect("database.db")
        cursor = database.cursor()
        cursor.executescript(sql_script)
        database.commit()
        database.close()
    except sqlite3.Error as err:
        print(err)

    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    initalize_db()
