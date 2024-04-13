from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User

def add_to_wishlist(username, game_id, repo: AbstractRepository):
    # Check if user and game exist, then add game to user's wishlist
    user = repo.get_user(username)
    game = repo.get_game_id(game_id)
    if user and game:
        user.add_favourite_game(game)


def remove_from_wishlist(username, game_id, repo: AbstractRepository):
    # Check if user exists, then remove game from user's wishlist
    user = repo.get_user(username)
    game = repo.get_game_id(game_id)
    if user and game:
        user.remove_favourite_game(game)


def get_wishlist(username, repo: AbstractRepository):
    # Get the user's wishlist
    user = repo.get_user(username)
    if user:
        return user.favourite_games
    return []


def get_user_for_wishlist(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException
    return user