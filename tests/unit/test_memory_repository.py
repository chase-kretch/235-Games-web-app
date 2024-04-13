import pytest

from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.adapters.memory_repository import MemoryRepository

"""
This file is for unit testing of memory repository
Type 'python -m pytest' without quotation mark in terminal for testing
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



def test_repository_can_add_games(in_memory_repo):
    repo = MemoryRepository() # Creates repo instance, creates the game, then attempts to add the game
    game = create_game1()
    repo.add_game(game)
    assert game in repo.get_games()


def test_repo_can_retrieve_games(in_memory_repo):
    repo = MemoryRepository()
    game = create_game1()
    repo.add_game(game)
    assert repo.get_games()[0] == game # Checks if the game returned from the get_games is the correct one


def test_repo_can_get_num_games(in_memory_repo):
    repo = MemoryRepository()
    game = create_game1()
    game2 = create_game2()
    repo.add_game(game)
    repo.add_game(game2)
    assert repo.get_number_of_games() == 2 # Checks if we get 2 for 2 games


def test_repo_can_get_first_game(in_memory_repo):
    repo = MemoryRepository()
    game1 = create_game1()
    game2 = create_game2()
    repo.add_game(game1)
    repo.add_game(game2)
    assert repo.get_first_game() == game1 # Checks if we get game1 as our first game

def test_repo_can_get_last_game(in_memory_repo):
    repo = MemoryRepository()
    game1 = create_game1()
    game2 = create_game2()
    repo.add_game(game1)
    repo.add_game(game2)
    assert repo.get_last_game() == game2 # Checks if we get game2 as our last game

def test_repo_can_get_game_from_id(in_memory_repo):
    repo = MemoryRepository()
    game1 = create_game1()
    game2 = create_game2()
    repo.add_game(game1)
    repo.add_game(game2)
    assert repo.get_game_id(1) == game1  # Checks if we get game1 when we put in game1s ID
    assert repo.get_game_id(2) == game2  # Checks if we get game2 when we put in game2s ID\


def test_add_review_to_repo(in_memory_repo):
    repo = MemoryRepository()
    user = User("Shyamli", "pw12345")
    game = Game(1, "Domino Game")
    review1 = Review(user, game, 3, "Great game!")
    repo.add_review(review1)
    assert review1 in repo.get_reviews()
    assert review1 in user.reviews
    assert review1 in game.reviews

def test_get_review_from_repo(in_memory_repo):
    repo = MemoryRepository()
    user = User("Shyamli", "pw12345")
    game = Game(1, "Domino Game")
    review1 = Review(user, game, 3, "Great game!")
    repo.add_review(review1)
    assert repo.get_reviews()[0] == review1

def test_change_password(in_memory_repo):
    # Testing change password function
    repo = MemoryRepository()
    username = "Shyamli"
    password = "pw12345"
    user = User(username, password)
    repo.add_user(user)
    new_password = "54321wp"
    repo.change_password(user, new_password)
    assert repo.get_user(username).password == new_password
    assert repo.get_user(username).password != password


def remove_user(in_memory_repo):
    # Testing remove user function
    # It should remove user and all the related reviews from that user
    repo = MemoryRepository()
    username = "Shyamli"
    password = "pw12345"
    user = User(username, password)
    repo.add_user(user)
    game = Game(1, "Domino Game")
    review1 = Review(user, game, 3, "Great game!")
    review2 = Review(User("test", "54321wp"), game, 3, "Great game!")
    repo.add_review(review1)
    repo.add_review(review2)
    assert repo.get_user(username) == user
    assert repo.get_reviews()[0] == review1
    repo.remove_user(user)
    assert repo.get_user(username) == None
    assert repo.get_reviews()[0] == review2
