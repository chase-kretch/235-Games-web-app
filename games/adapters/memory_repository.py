import os.path
from bisect import insort_left
from typing import List
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, User, Review
from games.adapters.datareader.csvdatareader import GameFileCSVReader, UserFileCSVReader

class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._games = list()
        self._users = list()
        self._reviews = list()

    def add_game(self, game: Game):
        if isinstance(game, Game):
            insort_left(self._games, game)

    def get_number_of_games(self):
        return len(self._games)

    def get_games(self) -> List[Game]:
        return self._games

    def get_first_game(self):
        return self._games[0]

    def get_last_game(self):
        return self._games[-1]

    def get_game_id(self, game_id: int) -> Game:
        for game in self._games:
            if game.game_id == game_id:
                return game
        return None

    def add_user(self, user: User):
        if isinstance(user, User):
            self._users.append(user)

    def get_user(self, username):
        username = username.lower().strip()
        return next((user for user in self._users if user.username == username), None)

    def change_password(self, user: User, password: str):
        user.password = password


    def remove_user(self, user: User):
        for i in reversed(range(len(self._reviews))):
            review = self._reviews[i]
            game = review.game
            if review.user == user:
                user.remove_review(review)
                game.remove_review(review)
                self._reviews.remove(review)
        self._users.remove(user)


    def add_review(self, review: Review):
        if isinstance(review, Review):
            self._reviews.append(review)
        game = review.game
        game.add_review(review)
        user = review.user
        user.add_review(review)
        print(self._reviews)

    def get_reviews(self):
        return self._reviews

    def get_wishlist(self, username) -> list[Game]:
        user = self.get_user(username)
        return user.favourite_games

    def add_game_to_wishlist(self, username, game_id):
        game = self.get_game_id(game_id)
        user = self.get_user(username)
        user.favourite_games.append(game)

    def remove_game_from_wishlist(self, username, game_id):
        user = self.get_user(username)
        game = self.get_game_id(game_id)
        user.favourite_games.remove(game)

# Code that used for populating has moved to repository_populate.py