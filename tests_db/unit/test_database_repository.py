import pytest

import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import User, Game, Review, Genre, Publisher
from games.adapters.repository import RepositoryException


"""
This file is for unit testing of methods in database_repository
Type 'python -m pytest' without quotation mark in terminal to test everything
Type 'python -m pytest tests_db' without quotation mark in terminal to test functionality related with database
"""

# Creates 2 games to use for testing


def create_game1():
    test_game = Game(1, "Call of Duty® 4: Modern Warfare®")
    test_game.release_date = "Nov 12, 2007"
    test_game.price = 9.99
    test_game.description = "The new action-thriller from the award-winning team at Infinity Ward, the creators of " \
                            "the Call of Duty® series, delivers the most intense and cinematic action experience ever. "
    test_game.image_url = "https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118"
    test_game.genre = Genre("Shooter")
    test_game.publisher = Publisher("Activision")
    return test_game


def create_game2():
    test_game = Game(2, "Terraria")
    test_game.release_date = "May 12, 2011"
    test_game.price = 11.99
    test_game.description = "Dig, fight, explore, build! Nothing is impossible in this action-packed adventure game. Four Pack also available!"
    test_game.image_url = "https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118"
    test_game.genre = Genre("Sandbox")
    test_game.publisher = Publisher("Re-Logic")
    return test_game


def test_repository_can_add_user(session_factory):
    repos = SqlAlchemyRepository(session_factory)
    user = User('Dave', 'ABCdef1234')
    repos.add_user(user)

    check = repos.get_user('Dave')

    assert check == user and check is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('admin')

    assert user == User('admin', 'ABCdef1234')


def test_repository_does_not_retrieve_non_existant_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('prince')

    assert user is None


def test_repository_can_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('Shyamli', 'pw12345')
    game = create_game1()
    review = Review(user, game, 5, "This is a great game!")
    repo.add_user(user)
    repo.add_game(game)
    repo.add_review(review)
    retrieved_review = repo.get_reviews(game.game_id)
    assert retrieved_review == [review]


def test_repository_can_get_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('Shyamli', 'pw12345')
    game = create_game1()
    review1 = Review(user, game, 5, "This is a great game!")
    review2 = Review(user, game, 1, "This is a bad game!")
    repo.add_user(user)
    repo.add_game(game)
    repo.add_review(review1)
    repo.add_review(review2)
    retrieved_review = repo.get_reviews(game.game_id)
    assert retrieved_review == [review1, review2]


def test_repo_can_add_game_to_wishlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('Shyamli', 'pw12345')
    game1 = create_game1()
    game2 = create_game2()
    repo.add_user(user)
    repo.add_game(game1)
    repo.add_game(game2)
    repo.add_game_to_wishlist('Shyamli', game1.game_id)
    repo.add_game_to_wishlist('Shyamli', game2.game_id)
    user_wishlist = repo.get_wishlist('Shyamli')
    assert user_wishlist == [game1, game2]
    # add game that is already in wishlist
    repo.add_game_to_wishlist('Shyamli', game2.game_id)
    user_wishlist = repo.get_wishlist('Shyamli')
    assert user_wishlist == [game1, game2]


def test_repo_can_remove_game_from_wishlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('Shyamli', 'pw12345')
    game1 = create_game1()
    game2 = create_game2()
    repo.add_user(user)
    repo.add_game(game1)
    repo.add_game(game2)
    repo.add_game_to_wishlist('Shyamli', game1.game_id)
    repo.add_game_to_wishlist('Shyamli', game2.game_id)
    repo.remove_game_from_wishlist('Shyamli', game2.game_id)
    user_wishlist = repo.get_wishlist('Shyamli')
    assert user_wishlist == [game1]
    # remove game that is not in wishlist
    repo.remove_game_from_wishlist('Shyamli', game2.game_id)
    user_wishlist = repo.get_wishlist('Shyamli')
    assert user_wishlist == [game1]


def test_repository_can_get_wishlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('Shyamli', 'pw12345')
    game1 = create_game1()
    game2 = create_game2()
    repo.add_user(user)
    repo.add_game(game1)
    repo.add_game(game2)
    repo.add_game_to_wishlist('Shyamli', game1.game_id)
    repo.add_game_to_wishlist('Shyamli', game2.game_id)
    user_wishlist = repo.get_wishlist('Shyamli')
    assert user_wishlist == [game1, game2]


def test_repository_can_add_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game = create_game1()
    repo.add_game(game)
    assert game in repo.get_games()


def test_repo_can_retrieve_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game = create_game1()
    repo.add_game(game)
    assert repo.get_games()[0] == game


def test_repo_can_get_num_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.get_number_of_games() == 877  # there are 877 games in the csv


def test_repo_can_get_last_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    last_game = Game(2073470, "Kanjozoku Game レーサー")
    assert repo.get_last_game() == last_game


def test_repo_can_get_first_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    first_game = Game(3010, "Xpand Rally")
    assert repo.get_first_game() == first_game


def test_repo_can_get_game_by_game_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game = Game(3010, "Xpand Rally")
    assert repo.get_game_id(3010) == game


def test_repo_can_change_password(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    username = "Shyamli"
    password = "pw12345"
    user = User(username, password)
    repo.add_user(user)
    new_password = "54321wp"
    repo.change_password(user, new_password)
    assert repo.get_user(username).password == new_password
    assert repo.get_user(username).password != password


def test_repo_can_get_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    games = repo.get_games()
    first_game = Game(3010, "Xpand Rally")
    last_game = Game(2073470, "Kanjozoku Game レーサー")
    assert len(games) == 877
    assert games[0] == first_game
    assert games[-1] == last_game


def test_repo_can_remove_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    username = "Shyamli"
    password = "pw12345"
    user = User(username, password)
    game = create_game1()
    review1 = Review(user, game, 5, "This is a great game!")
    review2 = Review(User("test", "54321wp"), game, 3, "Great game!")
    repo.add_user(user)
    repo.add_game(game)
    repo.add_review(review1)
    repo.add_review(review2)
    assert repo.get_user(username) == user
    assert repo.get_reviews(1)[0] == review1
    repo.remove_user(user)
    assert repo.get_user(username) == None
    assert repo.get_reviews(1)[0] == review2
