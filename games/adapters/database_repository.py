from datetime import date
from typing import List
import os
from sqlalchemy import desc,asc
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from games.domainmodel.model import User, Game, Review, Wishlist, Publisher
from games.adapters.repository import AbstractRepository
from games.adapters.datareader.csvdatareader import GameFileCSVReader, UserFileCSVReader

class SessionContextmanager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)


    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        return self.__session.commit()

    def rollback(self):
        return self.__session.rollback()

    def reset_session(self): # This method can be used to start a new session each http request. (before_request callback)
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextmanager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user_name = user_name.lower()
            user = self._session_cm.session.query(User).filter(User._User__username == user_name).one() # Needs to be read from orm??
        except NoResultFound:
            pass
        return user

    def add_review(self, review: Review):
        #super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews(self, id: int):
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def add_game_to_wishlist(self, username, game_id):
        with self._session_cm as scm:
            username = username.lower()
            user = scm.session.query(User).filter(User._User__username == username).one()
            game = scm.session.query(Game).filter(Game._Game__game_id == game_id).one()
            if game not in user.favourite_games:
                user.favourite_games.append(game)
                scm.commit()

    def remove_game_from_wishlist(self, username, game_id):
        with self._session_cm as scm:
            username = username.lower()
            user = scm.session.query(User).filter(User._User__username == username).one()
            game = scm.session.query(Game).filter(Game._Game__game_id == game_id).one()
            if game in user.favourite_games:
                user.favourite_games.remove(game)
                scm.commit()

    def get_wishlist(self, username):
        with self._session_cm as scm:
            username = username.lower()
            user = scm.session.query(User).filter(User._User__username == username).one()
            return user.favourite_games

    def add_game(self, game: Game):
        """Convert the list of languages to a comma-separated string
        languages_str = ', '.join(game.languages) if game.languages else None
        game.languages = languages_str"""
        with self._session_cm as scm:
            scm.session.add(game)
            scm.commit()

    def get_game(self, id: int):
        game = None
        try:
            game = self._session_cm.session.query(Game).filter(Game._Game__game_id == id).one()
            # Split the comma-separated string into a list of languages
            # game.languages = game.languages.split(', ') if game.languages else []
        except NoResultFound:
            pass
        return game

    def get_number_of_games(self):
        number_of_games = self._session_cm.session.query(Game).count()
        return number_of_games


    # These need to be implemented but its kinda confusing atm

    def get_last_game(self):
        games = self._session_cm.session.query(Game).all()
        return games[-1]

    def get_first_game(self):
        games = self._session_cm.session.query(Game).all()
        return games[0]

    def get_game_id(self, game_id: int) -> Game:
        try:
            return self._session_cm.session.query(Game).filter(Game._Game__game_id == game_id).one()
        except NoResultFound:
            return None

    def change_password(self, user: User, password: str):
        with self._session_cm as scm:
            scm.session.query(User).filter(User._User__username == user.username).update({'_User__password': password})
            scm.commit()

    def get_games(self) -> List[Game]:
        games = self._session_cm.session.query(Game).all()
        return games

    def remove_user(self, user: User):
        with self._session_cm as scm:
            # Delete connected reviews
            for i in reversed(range(len(user.reviews))):
                scm.session.delete(user.reviews[i])
            # Delete connected wishlists
            for i in reversed(range(len(user.favourite_games))):
                user.favourite_games.remove(user.favourite_games[i])
            # Delete user and commit the change
            scm.session.delete(user)
            scm.commit()


# Code that used for populating has moved to repository_populate.py