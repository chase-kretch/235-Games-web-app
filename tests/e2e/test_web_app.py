import pytest
from flask import session

"""
This file is for end to end testing of the website we built
Type 'python -m pytest' without quotation mark in terminal for testing
"""


def test_adding_and_display_review(client, auth):
    # Needs to be done
    auth.login()
    response = client.get('review/435790')
    assert response.status_code == 200
    response = client.post('review/435790', data={'review': 'great', 'rating': 1, 'game_id': 435790})
    assert response.status_code == 302
    assert response.headers['Location'] == '/description/435790'
    response = client.get('/description/435790')
    assert b"great" in response.data

def test_invalid_review(client, auth):
    auth.login()
    response = client.get('review/435790')
    assert response.status_code == 200
    response = client.post('review/435790', data={'review': '', 'rating': 0, 'game_id': 435790})
    assert response.status_code == 200


def test_review_html(client, auth):
    auth.login()
    response = client.get('review/435790')
    assert response.status_code == 200
    assert b"10 Second Ninja X" in response.data

def test_review_in_profile_reviews(client, auth):
    # Needs to be done
    auth.login()
    response = client.get('review/435790')
    assert response.status_code == 200
    response = client.post('review/435790', data={'review': 'great', 'rating': 1, 'game_id': 435790})
    assert response.status_code == 302
    assert response.headers['Location'] == '/description/435790'
    response = client.get('/profile/reviews')
    assert b"great" in response.data


def test_wishlist(client, auth):
    auth.login()
    response = client.get('/description/435790')
    assert response.status_code == 200
    assert b"Add to Wishlist" in response.data
    assert b"10 Second Ninja X" in response.data
    response = client.post('/wishlist/toggle_wishlist', data={'game_id': 435790, 'action': 'add'},
                           follow_redirects=True)
    assert response.status_code == 200
    response = client.get('/description/435790')
    assert b"Remove from Wishlist" in response.data
    response = client.get('/wishlist/')
    assert response.status_code == 200
    assert b"10 Second Ninja X" in response.data



def test_index(client):
    # testing home page
    response = client.get("/")
    assert response.status_code == 200
    assert b'CS235 Game Library' in response.data


def test_games_with_id(client):
    # Testing getting games page without paramater
    response = client.get("/games")
    assert response.status_code == 200
    assert b'10 Second Ninja X' in response.data

    # Testing getting games page with id parameter
    response = client.get("/games?id=855010")
    assert response.status_code == 200
    assert b'270 | Two Seventy US Election' in response.data

    # Testing getting games page with wrong id parameter
    # It should return the first page
    response = client.get("/games?id=99999999999999999999999999")
    assert response.status_code == 200
    assert b'10 Second Ninja X' in response.data


def test_games_with_genre(client):
    # Testing getting games by genre page
    response = client.get("/genre/Action")
    assert response.status_code == 200
    assert b'10 Second Ninja X' in response.data
    response = client.get("genre/Adventure")
    assert response.status_code == 200
    assert b'1000 Amps' in response.data


def test_games_with_search(client):
    # Testing searching game with keyword "100"
    response = client.get("/search?criteria=all&genre=all&language=all&query=100")
    assert response.status_code == 200
    assert b'100 Doors: Escape from Work' in response.data

    # Testing searching game with keyword "angry" for title that is action game and supports English
    response = client.get("/search?criteria=title&genre=Action&language=English&query=angry")
    assert response.status_code == 200
    assert b'Angry King' in response.data


def test_description(client):
    # Testing if getting description page works
    response = client.get("/description/435790")
    assert response.status_code == 200
    assert b'10 Second Ninja X' in response.data
    assert b'10 SECOND NINJA X is a shockingly fast, overwhelmingly intense action/puzzle game.' in response.data


def test_register(client):
    # Testing getting register form
    response = client.get("/authentication/register")
    assert response.status_code == 200
    # Testing posting register form
    response = client.post("/authentication/register", data={'user_name': 'testvalue', 'password': 'PassWord1234'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Please enter the username'),
        ('test', '', b'Please enter the password'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('admin', 'Test123456', b'')
))

def test_register_with_invalid_input(client, username, password, message):
    # Test registering with various invalid input
    response = client.post("/authentication/register", data={'user_name': username, 'password': password})
    assert message in response.data
    assert response.status_code == 200


def test_profile(client, auth):
    # Testing getting a profile page
    auth.login()
    response = client.get("/profile/")
    assert response.status_code == 200
    assert b"Hello admin" in response.data and b"Reviews" in response.data and b"Change a password" in response.data and b"Delete the account" in response.data

    # Testing getting a profile page without login
    auth.logout()
    response = client.get("/profile/")
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'

    # Testing reviews page
    auth.login()
    response = client.get("/profile/reviews")
    assert response.status_code == 200
    assert b'This page shows you all the reviews you have left!' in response.data

    # Testing wishlist page
    response = client.get("/wishlist/")
    assert response.status_code == 200
    assert b'This page shows you all the games in your wishlist!' in response.data

    # Testing change password page
    response = client.post("/authentication/change_password", data={'old_password': "ABCdef1234", 'new_password1': 'abcDEF1234', 'new_password2': 'abcDEF1234'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/profile/'

    # Testing delete account
    response = client.get("/profile/delete_account?confirm=False")
    assert response.status_code == 200
    assert b"Are you sure you want to delete your account?" in response.data
    response = client.get("/profile/delete_account?confirm=True")
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/logout'


def test_login(client, auth):
    # Testing getting login page
    response = client.get("/authentication/login")
    assert response.status_code == 200
    assert b"Login" in response.data

    # Testing succesful login
    response = auth.login()
    assert response.headers['Location'] == '/'
    with client:
        client.get('/')
        assert session['username'] == "admin"


def test_logout(client, auth):
    # Testing succesful logout
    auth.login()
    with client:
        client.get('/')
        assert 'username' in session
        # Logout
        auth.logout()
        assert 'username' not in session