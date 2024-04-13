from werkzeug.security import generate_password_hash, check_password_hash

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass

class DifferentPasswordException(Exception):
    pass


def add_user(user_name: str, password: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is not None:
        raise NameNotUniqueException

    # Encrypt password so that the database doesn't store passwords 'in the clear'.
    password_hash = generate_password_hash(password)

    # Create and store the new User, with password encrypted.
    user = User(user_name, password_hash)
    repo.add_user(user)


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def authenticate_user(username: str, password: str, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(username)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException
    return authenticated


# ===================================================
# Functions to convert model entities to dictionaries
# ===================================================

def user_to_dict(user: User):
    user_dict = {
        'username': user.username,
        'password': user.password
    }
    return user_dict

# ===================================================
# Wishlist functions
# ===================================================





def change_password(username: str, password1: str, password2: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if password1 != password2:
        raise DifferentPasswordException
    password_hash = generate_password_hash(password1)
    repo.change_password(user, password_hash)