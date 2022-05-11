from urllib import request

import pytest
import os
from app import db, auth, create_database
from app.db.models import User
from app.auth.forms import csv_upload
from flask_login import FlaskLoginClient

from flask_login import current_user

from app.db.models import User, products, Cars

from app.db import db
from app import create_app
from tests.click_test import runner

"""Tests for Project 2"""
test_email = "tobedeleted@tobedeleted.com"
test_password = "Password123"


# Test 1
@pytest.mark.parametrize(
    ("email", "password", "message"),
    (("j@j.com", "sdgfhkjnsdf", b"Invalid username or password"),
     ("j@j.com", "agvjhhgbghkk", b"Invalid username or password")),
)
def test_bad_password_login(client, email, password, message):
    response = client.post("/login", data={"email": email, "password": password}, follow_redirects=True)
    assert response.status_code == 200
    assert message in response.data


# Test 2
@pytest.mark.parametrize(
    ("email", "password", "message"),
    (("a@a.com", "test", b"Invalid username or password"),
     ("test@test.com", "a", b"Invalid username or password")),
)
def test_bad_username_email_login(client, email, password, message):
    response = client.post("/login", data=dict(email=email, password=password), follow_redirects=True)
    assert message in response.data
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


# Test 3
@pytest.mark.parametrize(
    ("username", "password", "confirm", "message"),
    (("test1", "test123", "test123", b"Invalid email address."),
     ("test2", "test123", "test123", b"Invalid email address.")),
)
def test_bad_username_email_registration(client, username, password, confirm, message):
    response = client.post("/register", data=dict(email=username, password=password, confirm=confirm),
                           follow_redirects=True)
    assert message in response.data


# Test 4
@pytest.mark.parametrize(
    ("email", "password", "confirm"),
    (("j@j.com", "test123", "test1234"),
     ("a@a.com", "a12345", "a123456")),
)
def test_password_confirmation_registration(client, email, password, confirm):
    response = client.post("/register", data=dict(email=email, password=password, confirm=confirm),
                           follow_redirects=True)
    assert b"Passwords must match" in response.data


# Test 5
@pytest.mark.parametrize(
    ("username", "password", "confirm"),
    (("j@j.com", "test", "test"),
     ("a@a.com", "a", "a")),
)
def test_bad_password_criteria_registration(client, username, password, confirm):
    response = client.post("/register", data=dict(email=username, password=password, confirm=confirm),
                           follow_redirects=True)
    assert b"Field must be between 6 and 35 characters long." in response.data


# Test 6
def test_already_registered(client):
    email = "test1@test1.com"
    password = "test123"
    response = client.post("/register", data=dict(email=email, password=password, confirm=password),
                           follow_redirects=True)
    response2 = client.post("/register", data=dict(email=email, password=password, confirm=password),
                            follow_redirects=True)
    assert b"Already Registered" in response2.data


# Test 7
def test_successful_login(client):
    client.post("/register", data=dict(email=test_email, password=test_password, confirm=test_password),
                follow_redirects=True)
    response = client.post("/login", data={"email": test_email, "password": test_password}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome" in response.data


# Test 8
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


# Test 9
def test_deny_dashboard_access_for_logged_users(client):
    response = client.post("/dashboard", follow_redirects=True)
    assert response.status_code == 405


# Test 10
def test_dashboard_access_for_logged_users(client):
    client.post("/login",
                data={"email": "j@j.com", "password": "123456", "confirm": "123456"},
                follow_redirects=True)
    response = client.post("/dashboard", follow_redirects=True)
    assert response.status_code == 405


# Test 11
def test_failed_cvs(client):
    response = client.get('locations/uploads')
    assert response.status_code == 404  # User isn't logged in since we don't have a test_client
    assert db.session.query(User).count() == 0


# Test 12
def test_upload_locations(application):
    application.test_client_class = FlaskLoginClient
    user = User('admin@admin.com', 'Admin123', 1)
    db.session.add(user)
    db.session.commit()

    assert user.email == 'admin@admin.com'
    assert db.session.query(User).count() == 1

    root = os.path.dirname(os.path.abspath(__file__))
    locations = os.path.join(root, '../uploads/us_cities_short.csv')

    with application.test_client(user=user) as client:
        response = client.get('/locations/upload')
        assert response.status_code == 200

        form = csv_upload()
        form.file = locations
        assert form.validate


# Test 13
def test_dashboard_access(application):
    application.test_client_class = FlaskLoginClient
    user = User('sample@sample.com', 'testtest', 1)
    db.session.add(user)
    db.session.commit()
    assert user.email == 'sample@sample.com'
    assert db.session.query(User).count() == 1
    with application.test_client(user=user) as client:
        response = client.get('/dashboard')
        assert b'sample@sample.com' in response.data
        assert response.status_code == 200


# def test_deny_dashboard(application):
#     assert db.session.query(User).count() == 0
#     with application.test_client() as client:
#         response = client.get('/dashboard')
#         assert response.status_code == 302

# Test 14
def test_deny_dashboard(application):
    application.test_client_class = FlaskLoginClient
    assert db.session.query(User).count() == 0
    with application.test_client(user=None) as client:
        response = client.get('/dashboard')
        assert response.status_code == 302


# Test 15
def test_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/about"' in response.data
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data


# Test 16
def test_adding_car(application):
    with application.app_context():
        assert db.session.query(Cars).count() == 0
        # create a record
        car = Cars('Ford', 'Focus', "2020", '187893', 'car', 'img')
        # add it to get ready to be committed
        db.session.add(car)
        car = Cars.query.filter_by(car_maker='Ford').first()
        # asserting that the car_maker retrieved is correct
        assert car.car_maker == "Ford"


# Test 17
def test_create_database():
    response = runner.invoke(create_database)
    assert response.exit_code == 0
    location = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(location, '../database')
    assert os.path.exists(dir) == True


# Test 18
def test_deleting_car(application):
    with application.app_context():
        assert db.session.query(Cars).count() == 0
        car = Cars('Ford', 'Focus', "2020", '187893', 'car', 'img')
        # add it to get ready to be committed
        db.session.add(car)
        car = Cars.query.filter_by(car_maker='Ford').first()
        # asserting that the car_maker retrieved is correct
        assert car.car_maker == "Ford"
