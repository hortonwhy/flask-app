""" Module for testing all of lite.py """
import sys

sys.path.append("../")
from lite import get_db_connection, get_author_name, get_author_id
from lite import get_post, get_all_posts, get_all_users
from lite import validate_login, create_user, create_post
from lite import delete_post, edit_post, is_admin
from sqlite3 import Connection
import sqlite3
import pytest
from initdb import initalize_db

initalize_db()


def test_db_connection():
    assert isinstance(get_db_connection(), sqlite3.Connection)


def test_get_author_name_valid():
    assert get_author_name(1) == (("Wyatt", "Horton"))
    assert get_author_name(email="hortonwhy@gmail.com") == (("Wyatt", "Horton"))


def test_get_author_name_invalid():
    assert get_author_name(3) == (False)
    assert get_author_name(email="hortonwhy8@gmail.com") == (False)


def test_get_author_id():
    assert get_author_id("hortonwhy@gmail.com") == (1)
    assert get_author_id("hortonwhy98@gmail.com") == (False)


def test_get_post():
    assert isinstance(get_post(2), sqlite3.Row)
    assert isinstance(get_post("2"), sqlite3.Row)
    assert get_post(100) == None
    assert get_post("string") == None


def test_get_all_posts():
    assert isinstance(get_all_posts(), dict)
    assert len(get_all_posts()) == 2


def test_get_all_users():
    assert isinstance(get_all_users(), dict)
    assert len(get_all_users()) == 2


def test_validate_login():
    assert validate_login("hortonwhy@gmail.com", "123")
    assert validate_login("hortonwhy@gmail.com", "12494") == (False)
    assert validate_login(1904109490, 19040914109) == (False)


def test_create_user():
    assert create_user("Jim", "Boebert", "bill@email.com", "12345")
    assert len(get_all_users()) == 3
    with pytest.raises(TypeError):
        create_user("Jim", "Boebert", "12345")


def test_create_post():
    assert create_post(1, "a world", "shattered")
    assert len(get_all_posts()) == 3
    with pytest.raises(TypeError):
        create_post(1, "a world")


def test_delete_post():
    assert delete_post(1)
    assert len(get_all_posts()) == 2
    assert delete_post(1)
    with pytest.raises(TypeError):
        assert delete_post()


def test_edit_post():
    assert edit_post(2, "a new", "change")
    assert len(get_all_posts()) == 2
    assert get_post(2)["title"] == "a new"
    assert get_post(2)["body"] == "change"
    with pytest.raises(TypeError):
        assert edit_post(2, "renewed")


def test_is_admin():
    assert is_admin("hortonwhy@gmail.com")
    assert is_admin("hortonwhy2@gmail.com") == (False)
