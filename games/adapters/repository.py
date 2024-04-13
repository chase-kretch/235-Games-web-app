import abc
from typing import List

from games.domainmodel.model import Game, User, Review

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f"RepositoryException: {message}")


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_game(self, game: Game):

        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:

        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self):

        raise NotImplementedError

    @abc.abstractmethod
    def get_first_game(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_game(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_id(self, game_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def change_password(self, user: User, password: str):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_user(self, user: User):
        raise NotImplementedError

    def get_reviews(self):
        raise NotImplementedError

    def add_review(self, review: Review):
        raise NotImplementedError


