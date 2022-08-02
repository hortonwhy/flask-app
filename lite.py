""" Module containing all methods for CRUD Ops on local DB"""
import sqlite3


def get_db_connection():
    """ Open a connection with local database """
    conn = None
    try:
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as err:
        print(err)
        if conn is not None:
            conn.close()
        return False


def get_author_name(author_id=None, email=None):
    """ return first and last name given an id """
    conn = get_db_connection()
    try:
        if email:
            query = "SELECT firstName, lastName from users WHERE email = ?"
            result = conn.execute(query, (email,)).fetchone()
        else:
            query = "SELECT firstName, lastName from users WHERE id = ?"
            result = conn.execute(query, (author_id,)).fetchone()
        if result:
            return (result["firstName"], result["lastName"])
        return False
    except sqlite3.Error as err:
        print(err)
        return False
    finally:
        conn.close()


def get_author_id(email):
    """ Given unique email, return the unique id of the author """
    conn = get_db_connection()
    try:
        query = "SELECT id from users WHERE email = ?"
        result = conn.execute(query, (email,)).fetchone()
        if result:
            return result["id"]
        return False
    except sqlite3.Error as err:
        print(err)
        return False
    finally:
        conn.close()


def get_post(post_id):
    """ Given a post id query and return relevant information """
    conn = get_db_connection()
    try:
        query = "SELECT * FROM posts WHERE id = ?"
        result = conn.execute(query, (post_id,)).fetchone()
        return result
    except sqlite3.Error as err:
        print(err)
        return False
    finally:
        conn.close()


def get_all_posts():
    """ Return a dictionary containing all posts in the database """
    conn = get_db_connection()
    try:
        query = "SELECT * from posts"
        result = conn.execute(query).fetchall()
        posts = {}
        for row in result:
            values = {}
            values["created"] = row["created"]
            values["id"] = row["id"]
            values["author"] = get_author_name(row["author"])
            values["author_id"] = row["author"]
            values["title"] = row["title"]
            values["body"] = row["body"]
            posts[row["id"]] = values
        return posts
    except sqlite3.Error as err:
        print(err)
        return False

    finally:
        conn.close()


def get_all_users():
    """ Return a dictionary containing all users in the database """
    conn = get_db_connection()
    try:
        query = "SELECT * from users"
        result = conn.execute(query).fetchall()
        users = {}
        for row in result:
            values = {}
            values["id"] = row["id"]
            values["fname"] = row["firstName"]
            values["lname"] = row["lastName"]
            values["email"] = row["email"]
            values["password"] = row["password"]
            values["created"] = row["created"]
            values["authed"] = row["authed"]
            users[row["id"]] = values
        return users
    except sqlite3.Error as err:
        print(err)
        return False

    finally:
        conn.close()


def validate_login(email, password):
    """ given user input, verify matching credentials with database """
    conn = get_db_connection()
    query = "SELECT * FROM users WHERE email = ?"
    result = conn.execute(query, (email,)).fetchone()
    if result and result["password"] == password:
        return True
    return False


def create_user(fname, lname, email, password):
    """ Given user info, attempt to insert record to local database """
    conn = get_db_connection()
    query = "INSERT INTO users(firstName, lastName, email, password) VALUES(?, ?, ?, ?)"
    try:
        conn.execute(query, (fname, lname, email, password))
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(err)
        return False

    finally:
        conn.close()


def create_post(author_id, title, body):
    """ Given parameters attempt to insert into posts table """
    conn = get_db_connection()
    try:
        query = "INSERT INTO posts(author, title, body) VALUES(?, ?, ?)"
        conn.execute(query, (author_id, title, body))
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(err)
        return False
    finally:
        conn.close()


def delete_post(post_id):
    """ Given post id find and delete the record from local DB """
    conn = get_db_connection()
    try:
        query = "DELETE FROM posts WHERE id = ?"
        conn.execute(query, (post_id,))
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(err)
        return False
    finally:
        conn.close()


def edit_post(post_id, title, body):
    """ Given post id find and update title and body from local db """
    conn = get_db_connection()
    try:
        query = """UPDATE posts SET created = (datetime('now','localtime')),
        title = ?, body = ? WHERE id = ?"""
        conn.execute(query, (title, body, post_id))
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(err)
        return False
    finally:
        conn.close()


def is_admin(email):
    """ Given a unique email, check if user is an admin or not """
    conn = get_db_connection()
    query = "SELECT authed from users WHERE email = ?"
    result = conn.execute(query, (email,)).fetchone()
    if result and result["authed"]:
        return True
    return False
