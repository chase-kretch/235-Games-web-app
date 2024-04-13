import pytest
import os
from games.authentication import services as authentication_services
from games.authentication.services import AuthenticationException, DifferentPasswordException, UnknownUserException, \
    NameNotUniqueException
from games.browse import services as browse_services
from games.description import services as description_services
from games.home import services as home_services
from games.profile import services as profile_services
from games.wishlist import services as wishlist_services
from games.domainmodel.model import Game, Genre, Publisher, Review, User
from games.adapters.memory_repository import MemoryRepository
from werkzeug.security import check_password_hash

"""
This file is for unit testing of service layers
Type 'python -m pytest' without quotation mark in terminal for testing
"""

"""
Testing service layer in authentication blueprint
"""


def test_add_user(in_memory_repo):
    # Testing add_user function in authentication service layer
    repo = in_memory_repo
    user_name = "Shyamli"
    password = "pw12345"
    authentication_services.add_user(user_name, password, repo)
    user = repo.get_user(username=user_name)
    assert user.username == user_name.lower().strip()
    assert check_password_hash(user.password, password)
    with pytest.raises(NameNotUniqueException):
        authentication_services.add_user(user_name, password, repo)


def test_authentication_and_get_user(in_memory_repo):
    # Testing authenticate function and get_user function in authentication service layer
    repo = in_memory_repo
    username = "Shyamli"
    password = "pw12345"
    authentication_services.add_user(username, password, repo)
    user_dict = authentication_services.get_user(username, repo)
    assert user_dict['username'] == username.lower().strip()
    assert check_password_hash(user_dict['password'], password)
    username = "nonexistentuser"
    with pytest.raises(UnknownUserException):
        authentication_services.get_user(username, repo)

    username2 = "test"
    password2 = "Pw12345"
    authentication_services.add_user(username2, password2, repo)
    assert authentication_services.authenticate_user(username2, password2, repo)
    wrong_password = "wrong1234"
    with pytest.raises(AuthenticationException):
        authentication_services.authenticate_user(username2, wrong_password, repo)

def test_user_to_dict(in_memory_repo):
    # Testing user_to_dict function in authentication service layer
    username = "Shyamli"
    password = "pw12345"
    user = User(username, password)
    user_dict = authentication_services.user_to_dict(user)
    assert user.username == user_dict['username']
    assert user.password == user_dict['password']


def test_add_to_wishlist(in_memory_repo):
    repo = in_memory_repo
    new_user = User("Shyamli", "pw12345")
    game = Game(1, "Domino Game")
    repo.add_game(game)
    repo.add_user(new_user)
    # Add game that is not in wishlist
    wishlist_services.add_to_wishlist("Shyamli", 1, repo)
    user = repo.get_user("Shyamli")
    fav_games = user.favourite_games
    assert fav_games == [game]
    # Add game that is already in wishlist
    wishlist_services.add_to_wishlist("Shyamli", 1, repo)
    assert fav_games == [game]


def test_remove_from_wishlist(in_memory_repo):
    repo = in_memory_repo
    new_user = User("Shyamli", "pw12345")
    game1 = Game(1, "Domino Game")
    game2 = Game(2, "Sudoku Game")
    repo.add_game(game1)
    repo.add_game(game2)
    repo.add_user(new_user)
    wishlist_services.add_to_wishlist("Shyamli", 1, repo)
    # Remove game that is already not on wishlist
    wishlist_services.remove_from_wishlist(username="Shyamli", game_id=2, repo=repo)
    user = repo.get_user("Shyamli")
    assert user.favourite_games == [game1]
    # Remove game that is in wishlist
    wishlist_services.remove_from_wishlist(username="Shyamli", game_id=1, repo=repo)
    user = repo.get_user("Shyamli")
    assert user.favourite_games == []


def test_get_wishlist(in_memory_repo):
    repo = in_memory_repo
    new_user = User("Shyamli", "pw12345")
    game = Game(1, "Domino Game")
    repo.add_game(game)
    repo.add_user(new_user)
    wishlist_services.add_to_wishlist("Shyamli", 1, repo)
    assert wishlist_services.get_wishlist(username="Shyamli", repo=repo) == [game]


def test_get_user_for_wishlist(in_memory_repo):
    repo = in_memory_repo
    new_user = User("Shyamli", "pw12345")
    repo.add_user(new_user)
    get_user = wishlist_services.get_user_for_wishlist(username="Shyamli", repo=repo)
    assert new_user == get_user


def test_change_password(in_memory_repo):
    repo = in_memory_repo
    username = "Shyamli"
    new_user = User(username, "pw12345")
    repo.add_user(new_user)
    new_password1 = "newpassword"
    new_password2 = "newpassword"
    authentication_services.change_password(username, new_password1, new_password2, repo)
    user_after_change = in_memory_repo.get_user(username)
    assert check_password_hash(user_after_change.password, new_password1)
    new_password1 = "newpassword1"
    new_password2 = "newpassword2"
    with pytest.raises(DifferentPasswordException):
        authentication_services.change_password(username, new_password1, new_password2, repo)

"""
Testing service layer in browse blueprint
"""


def test_can_get_games(in_memory_repo):
    # Test service layer returns an existing game objects
    # Test service layer retrieves correct number of game objects
    # Test returned game object has correct values

    # Uses get_number_of_games for testing
    numbers_of_games = browse_services.get_number_of_games(in_memory_repo)
    assert numbers_of_games == 877  # Total number of games using get_number_of_games

    # Uses get_games for testing
    games_as_dict = browse_services.get_games(in_memory_repo)
    assert len(games_as_dict) == 877  # Total number of games using get_games
    assert games_as_dict[1]["game_id"] == 7940
    assert games_as_dict[1]["title"] == "Call of Duty® 4: Modern Warfare®"
    assert games_as_dict[1]["game_url"] == "Nov 12, 2007"


def test_can_get_game_alphabetically(in_memory_repo):
    # Test service layer returns an existing game objects
    # Test only 5 games are retrieved from the service layer for the pagination functionality
    # Test returned game object has correct values
    # Test returned game objects are indeed alphabetically ordered
    # Test previous id and next id is correct for the pagination functionality

    # Uses get_first_game for testing
    first_game = browse_services.get_first_game(in_memory_repo)
    assert first_game.game_id == 435790
    assert first_game.title == "10 Second Ninja X"

    # Uses get_last_game for testing
    last_game = browse_services.get_last_game(in_memory_repo)
    assert last_game.game_id == 1580640
    assert last_game.title == "银魂：Silver Soul"
    assert first_game.title < last_game.title  # Check alphabetical order of first game and last game

    # Uses get_games_by_id for testing
    test_id = 435790  # Using first page as a test case
    test_games_in_page = 5  # Return 5 games in a list
    test_genre = "all"
    non_filtered_games_as_tuple = browse_services.get_games_by_id(test_id, test_games_in_page, in_memory_repo,
                                                                  test_genre)
    # I will do this later -> filtered_games_as_tuple
    assert isinstance(non_filtered_games_as_tuple, tuple)
    assert isinstance(non_filtered_games_as_tuple[0], list)
    assert len(non_filtered_games_as_tuple[0]) == 5  # Return 5 games for pagination
    assert non_filtered_games_as_tuple[0][0]["game_id"] == 435790
    assert non_filtered_games_as_tuple[0][0]["title"] == "10 Second Ninja X"
    assert isinstance(non_filtered_games_as_tuple[1], type(None)) and isinstance(non_filtered_games_as_tuple[2], int)
    assert non_filtered_games_as_tuple[1] == None  # First page so don't have previous id
    assert non_filtered_games_as_tuple[2] == 855010
    assert non_filtered_games_as_tuple[0][0]["title"] < non_filtered_games_as_tuple[0][1][
        "title"]  # Check alphabetical order


def test_get_games_using_search(in_memory_repo):
    # Test getting games for a search key 'title' AND 'publisher'
    # Test getting games for a search key ‘title’
    # Test getting games for a search key ‘publisher’
    # Test if it returns no games if it could not find games with certain search term

    test_search_query = "ape"
    test_search_genre = "all"
    # test_search_language = "all"
    # Testing if searching with both title and publisher returns correct games
    all_searched_games = browse_services.get_games_with_search(in_memory_repo, test_search_query, "all",
                                                               test_search_genre)
    assert all_searched_games[0].title == "100 Doors: Escape from Work"
    assert all_searched_games[1].title == "Adventure Apes and the Mayan Mystery"
    assert len(all_searched_games) == 17

    # Testing if searching with title returns correct games
    title_searched_games = browse_services.get_games_with_search(in_memory_repo, test_search_query, "title",
                                                                 test_search_genre)
    assert title_searched_games[0].title == "100 Doors: Escape from Work"
    assert title_searched_games[1].title == "Adventure Apes and the Mayan Mystery"
    assert len(title_searched_games) == 15

    # Testing if searching with publisher returns correct games
    publisher_searched_games = browse_services.get_games_with_search(in_memory_repo, test_search_query, "publisher",
                                                                     test_search_genre)
    assert publisher_searched_games[0].title == "Intergalactic Bubbles"
    assert publisher_searched_games[1].title == "Yousei Daisensou ~ Touhou Sangetsusei"
    assert len(publisher_searched_games) == 2

    # Testing if it returns nothing when service layer could not find anything related to search term
    empty_searched_games = browse_services.get_games_with_search(in_memory_repo, "abcd", "all", test_search_genre)
    assert len(empty_searched_games) == 0

    # Testing if it retunrs nothing when search term is not given
    empty_search_term_games = browse_services.get_games_with_search(in_memory_repo, None, "all", test_search_genre)
    assert len(empty_search_term_games) == 0


def test_get_games_using_genres(in_memory_repo):
    # Test service layer returns correct game objects with specified genre

    # Test getting games with genre Adventure
    test_genre1 = "Adventure"
    test_num_of_games = 5
    test_id_for_genre1 = browse_services.get_first_genre_game(in_memory_repo, test_genre1).game_id
    filtered_games_as_tuple1 = browse_services.get_games_by_id(test_id_for_genre1, test_num_of_games, in_memory_repo,
                                                               test_genre1)
    assert filtered_games_as_tuple1[1] == None
    assert filtered_games_as_tuple1[0][0]['game_id'] == test_id_for_genre1
    assert filtered_games_as_tuple1[0][0]['title'] == "1000 Amps"
    assert filtered_games_as_tuple1[0][1]['title'] == "A Blind Legend"

    # Test getting games with genre Sports
    test_genre2 = "Sports"
    test_id_for_genre2 = browse_services.get_first_genre_game(in_memory_repo, test_genre2).game_id
    filtered_games_as_tuple2 = browse_services.get_games_by_id(test_id_for_genre2, test_num_of_games, in_memory_repo,
                                                               test_genre2)
    assert filtered_games_as_tuple2[1] == None
    assert filtered_games_as_tuple2[0][0]['game_id'] == test_id_for_genre2
    assert filtered_games_as_tuple2[0][0]['title'] == "Automobilista 2"
    assert filtered_games_as_tuple2[0][1]['title'] == "Beaver Fun™ River Run - Steam Edition"


"""
Testing service layer in description blueprint
"""


def test_get_values_for_decription(in_memory_repo):
    # Test description service layer returns valid values for certain game
    # Test service layer returns correctly formatted review
    test_game_for_description = description_services.get_game_id(1241110, in_memory_repo)
    assert test_game_for_description['title'] == "ANARCHY"
    assert repr(test_game_for_description['publisher']) == "NewProjekt"
    assert test_game_for_description['genres'] == "Action, Adventure, Casual, Indie"


def test_add_review_desc_services(in_memory_repo):
    repo = in_memory_repo
    user = User("Shyamli", "pw12345")
    game = Game(1, "Domino Game")
    repo.add_game(game)
    repo.add_user(user)
    user1 = repo.get_user("shyamli")
    print(user1)
    review = Review(user, repo.get_game_id(1), 1, "great")
    description_services.add_review(1, "great", 1, "shyamli", repo)
    assert len(repo.get_reviews()) == 1
    assert repo.get_reviews()[0] == review


def test_get_game_from_desc_services(in_memory_repo):
    repo = MemoryRepository()
    user = User("Shyamli", "pw12345")
    game = Game(1, "Domino Game")
    # game.languages = []
    repo.add_game(game)
    repo.add_user(user)
    gametest = description_services.get_game_id(1, repo)
    assert gametest['game_id'] == 1


def test_review_to_dict(in_memory_repo):
    repo = MemoryRepository()
    user = User("Shyamli", "pw12345")
    game = Game(1, "Domino Game")
    # game.languages = []
    repo.add_game(game)
    repo.add_user(user)
    review = Review(user, repo.get_game_id(1), 1, "great")
    review_dict = description_services.review_to_dict(review)
    assert review_dict['username'] == "shyamli"
    assert review_dict['game'] == game
    assert review_dict['review_text'] == review.comment


def test_validity_of_review(in_memory_repo):
    repo = MemoryRepository()
    user = User("Shyamli", "pw12345")
    game = Game(1, "Domino Game")
    # game.languages = []
    repo.add_game(game)
    repo.add_user(user)
    review = Review(user, repo.get_game_id(1), 1, "great")
    repo.add_review(review)
    assert description_services.validity_of_review(1, "shyamli", repo) == False


"""
Testing service layer in home blueprint
"""


def test_get_unique_values(in_memory_repo):
    # Test getting unique genres
    # Test getting unique supported languages

    # Testing getting list of unique genres using get_unique_genres
    test_unique_genres = home_services.get_unique_genres(in_memory_repo)
    assert len(test_unique_genres) == 24
    assert repr(test_unique_genres[0]) == "Action"
    assert repr(test_unique_genres[1]) == "Adventure"
    assert repr(test_unique_genres[-1]) == "Web Publishing"

    '''Testing getting list of unique languages using get_unique_languages
    test_unique_languages = home_services.get_unique_languages(in_memory_repo)
    assert len(test_unique_languages) == 31
    assert test_unique_languages[0] == "Arabic"
    assert test_unique_languages[1] == "Bulgarian"
    assert test_unique_languages[-1] == "Vietnamese"
    assert "English" in test_unique_languages'''


def test_get_games_by_price(in_memory_repo):
    # Test getting list of games for certain price range

    # Test if the service layer returns list of free games using get_games_by_price
    test_free_games = home_services.get_games_by_price(in_memory_repo, -1, 0)
    assert len(test_free_games) == 125
    assert test_free_games[0].title == "270 | Two Seventy US Election"
    assert test_free_games[-1].game_id == 1986310

    # Test if the service layer returns list of under $5 games using get_games_by_price
    test_under_5_games = home_services.get_games_by_price(in_memory_repo, 0, 5)
    assert len(test_under_5_games) == 386
    assert test_under_5_games[0].title == "ARENA 8"
    assert test_under_5_games[-1].game_id == 1331390


"""
Testing service layer in profile blueprint
"""


def test_profile_get_user(in_memory_repo):
    repo = in_memory_repo
    new_user = User("Shyamli", "pw12345")
    repo.add_user(new_user)
    get_user = profile_services.get_user("Shyamli", repo=repo)
    user = repo.get_user("Shyamli")
    assert user == get_user
    with pytest.raises(profile_services.UnknownUserException):
        profile_services.get_user("nonexistentuser", repo=repo)


def test_delete_account(in_memory_repo):
    repo = in_memory_repo
    new_user = User("Shyamli", "pw12345")
    repo.add_user(new_user)
    profile_services.delete_account("Shyamli", repo=repo)
    assert repo.get_user("Shyamli") == None
