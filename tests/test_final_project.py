from email.mime import application
from urllib import request

import pytest
from flask_login import current_user
from app.db.models import User, products, Cars

from app.db import db
from app import create_app
from flask import g
from flask import session
import app

"""Tests for Project 2"""
test_email = "tobedeleted@tobedeleted.com"
test_password = "Password123"


@pytest.mark.parametrize(
    ("email", "password", "message"),
    (("j@j.com", "sdgfhkjnsdf", b"Invalid username or password"),
     ("j@j.com", "agvjhhgbghkk", b"Invalid username or password")),
)
def test_bad_password_login(client, email, password, message):
    response = client.post("/login", data={"email": email, "password": password}, follow_redirects=True)
    assert response.status_code == 200
    assert message in response.data


@pytest.mark.parametrize(
    ("email", "password", "message"),
    (("a@a.com", "test", b"Invalid username or password"),
     ("test@test.com", "a", b"Invalid username or password")),
)
def test_bad_username_email_login(client, email, password, message):
    response = client.post("/login", data=dict(email=email, password=password), follow_redirects=True)
    assert message in response.data
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


@pytest.mark.parametrize(
    ("username", "password", "confirm", "message"),
    (("test1", "test123", "test123", b"Invalid email address."),
     ("test2", "test123", "test123", b"Invalid email address.")),
)
def test_bad_username_email_registration(client, username, password, confirm, message):
    response = client.post("/register", data=dict(email=username, password=password, confirm=confirm),
                           follow_redirects=True)
    assert message in response.data


@pytest.mark.parametrize(
    ("email", "password", "confirm"),
    (("j@j.com", "test123", "test1234"),
     ("a@a.com", "a12345", "a123456")),
)
def test_password_confirmation_registration(client, email, password, confirm):
    response = client.post("/register", data=dict(email=email, password=password, confirm=confirm),
                           follow_redirects=True)
    assert b"Passwords must match" in response.data


@pytest.mark.parametrize(
    ("username", "password", "confirm"),
    (("j@j.com", "test", "test"),
     ("a@a.com", "a", "a")),
)
def test_bad_password_criteria_registration(client, username, password, confirm):
    response = client.post("/register", data=dict(email=username, password=password, confirm=confirm),
                           follow_redirects=True)
    assert b"Field must be between 6 and 35 characters long." in response.data


def test_already_registered(client):
    email = "test1@test1.com"
    password = "test123"
    response = client.post("/register", data=dict(email=email, password=password, confirm=password),
                           follow_redirects=True)
    response2 = client.post("/register", data=dict(email=email, password=password, confirm=password),
                            follow_redirects=True)
    assert b"Already Registered" in response2.data


def test_successful_login(client):
    client.post("/register", data=dict(email=test_email, password=test_password, confirm=test_password),
                follow_redirects=True)
    response = client.post("/login", data={"email": test_email, "password": test_password}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_successful_registration(client, application):
    response = client.post("/register",
                           data={"email": "user_to_be_delete@delete.org", "password": "test1234",
                                 "confirm": "test1234"},
                           follow_redirects=True)
    assert b"Congratulations, you are now a registered user!" in response.data
    with application.app_context():
        client.post("/login",
                    data={"email": "j@j.com", "password": "123456", "confirm": "123456"},
                    follow_redirects=True)
        user_to_delete = User.query.filter_by(email="user_to_be_delete@delete.org").first()
        response = client.post("/users/" + str(user_to_delete.get_id()) + "/delete", follow_redirects=True)
        assert response.status_code == 200


def test_deny_dashboard_access_for_logged_users(client):
    response = client.post("/dashboard", follow_redirects=True)
    assert response.status_code == 405


def test_dashboard_access_for_logged_users(client):
    client.post("/login",
                data={"email": "j@j.com", "password": "123456", "confirm": "123456"},
                follow_redirects=True)
    response = client.post("/dashboard", follow_redirects=True)
    assert response.status_code == 405


def test_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/about"' in response.data
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data


def test_adding_cars(application):
    with application.app_context():
        assert db.session.query(Cars).count() == 0

        # showing how to add a record
        # create a record
        car = Cars('Ford', 'Focus', "2020", '187893', 'car', 'img')
        # add it to get ready to be committed
        db.session.add(car)
        # call the commit
        # db.session.commit()
        # assert that we now have a new user
        # assert db.session.query(products).count() == 1
        # finding one user record by email
        car = Cars.query.filter_by(car_maker='Ford').first()
        # asserting that the car_maker retrieved is correct
        assert car.car_maker == "Ford"
