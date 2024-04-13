from games.adapters.memory_repository import AbstractRepository


class UnknownUserException(Exception):
    pass


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException
    return user


def delete_account(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    repo.remove_user(user)
