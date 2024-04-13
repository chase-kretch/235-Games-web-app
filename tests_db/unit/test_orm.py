import pytest
from sqlalchemy.exc import IntegrityError
from games.domainmodel.model import User, Game, Publisher, Genre, Wishlist, Review


"""
This file is for unit testing of orm
Type 'python -m pytest' without quotation mark in terminal to test everything
Type 'python -m pytest tests_db' without quotation mark in terminal to test functionality related with database
"""


def insert_user(empty_session, values=None):
    new_name = "test"
    new_password = "ABCdef1234"
    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',\
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT user_id from users where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT user_id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_publisher(empty_session):
    empty_session.execute('INSERT INTO publishers (name, publisher_id) VALUES ("testcompany", :publisher_id)',
                          {'publisher_id': 1}
                          )
    row = empty_session.execute('SELECT name from publishers').fetchone()
    return row[0]

def insert_genre(empty_session):
    empty_session.execute('INSERT INTO genres (genre_name) VALUES ("testgenre")')
    row = empty_session.execute('SELECT genre_id from genres').fetchone()
    return row[0]

def insert_game_genre_associations(empty_session, game_key, genre_key):
    empty_session.execute('INSERT INTO game_genres (game_id, genre_id) VALUES (:game_id, :genre_id)',
                          {'game_id': game_key, 'genre_id': genre_key}
                          )

def insert_game(empty_session):
    publisher_key = insert_publisher(empty_session)
    genre_key = insert_genre(empty_session)
    empty_session.execute('INSERT INTO games (game_id, title, price, release_date, publisher_name, genres) VALUES'
                          '(:game_id, "testgame", :price, "Nov 12, 2007", :publisher_name, :genres)',
                          {'game_id': 1, 'price':9.99, 'publisher_name':publisher_key, 'genres':genre_key}
    )
    row = empty_session.execute('SELECT game_id from games').fetchone()
    return row[0]

def insert_review(empty_session, game_key, user_key, values=None):
    comment = "Good!"
    rating = 5
    if values is not None:
        comment = values[0]
        rating = values[1]
    empty_session.execute('INSERT INTO reviews (game_id, comment, rating, user_id) VALUES (:game_id, :comment, :rating, :user_id)',
                          {'game_id': game_key, 'comment': comment, 'rating': rating, 'user_id': user_key}
                          )
    row = empty_session.execute('SELECT review_id from reviews').fetchone()
    return row[0]

def test_loading_of_users(empty_session):
    users = []
    users.append(('test', 'ABCdef1234'))
    users.append(('test2', 'abcDEF1234'))
    insert_users(empty_session, users)
    assert empty_session.query(User).all() == [User('test', 'ABCdef1234'), User('test2', 'abcDEF1234')]

def test_saving_of_users(empty_session):
    test_user = User('test', 'ABCdef1234')
    empty_session.add(test_user)
    empty_session.commit()
    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [('test', 'ABCdef1234')]

    with pytest.raises(IntegrityError):
        test_user2 = User('test', 'newPassword1234')
        empty_session.add(test_user2)
        empty_session.commit()

def test_saving_and_loading_of_game(empty_session):
    game_key = insert_game(empty_session)
    genre_key = insert_genre(empty_session)
    insert_game_genre_associations(empty_session, game_key, genre_key)
    empty_session.commit()
    game = empty_session.query(Game).get(game_key)
    genre = empty_session.query(Genre).get(genre_key)
    expected_game = Game(1, "testgame")
    expected_genre = Genre("testgenre")
    expected_publisher = Publisher("testcompany")
    assert game == expected_game
    assert game_key == game.game_id
    assert genre == expected_genre
    assert game.genres == [expected_genre]
    assert game.publisher == expected_publisher

def test_saving_and_loading_of_reviews(empty_session):
    game_key = insert_game(empty_session)
    user_key1 = insert_user(empty_session)
    user_key2 = insert_user(empty_session, ["anotheruser", "Password1234"])
    review_key = insert_review(empty_session, game_key, user_key1)
    empty_session.commit()
    fetched_review = empty_session.query(Review).get(review_key)
    fetched_user1 = empty_session.query(User).get(user_key1)
    fetched_user2 = empty_session.query(User).get(user_key2)
    fetched_game = empty_session.query(Game).get(game_key)
    assert fetched_review.rating == 5
    assert fetched_review.comment == "Good!"
    assert fetched_review.user == fetched_user1
    assert fetched_review.game == fetched_game

    review2 = Review(fetched_user2, fetched_game, 1, "Terrible game!")
    empty_session.add(review2)
    empty_session.commit()
    fetched_reviews = empty_session.query(Review).all()
    fetched_review2 = fetched_reviews[1]
    assert fetched_review2.rating == 1
    assert fetched_review2.comment == "Terrible game!"
    assert fetched_review2.user == fetched_user2
    assert fetched_review2.game == fetched_game

    assert fetched_review != fetched_review2
    assert fetched_review.user != fetched_review2.user
    assert fetched_review.game == fetched_review2.game


def test_loading_and_saving_publishers(empty_session):
    game_key = insert_game(empty_session)
    empty_session.commit()
    fetched_game = empty_session.query(Game).get(game_key)
    fetched_publisher1 = empty_session.query(Publisher).get(1)
    assert fetched_publisher1.publisher_name == "testcompany"
    assert fetched_game.publisher == fetched_publisher1

    new_publisher = Publisher("anothercompany")
    empty_session.add(new_publisher)
    empty_session.commit()
    # publisher id is 2 because it autoincrement
    fetched_publisher2 = empty_session.query(Publisher).get(2)
    assert fetched_publisher2.publisher_name == "anothercompany"
    assert fetched_publisher2 == new_publisher