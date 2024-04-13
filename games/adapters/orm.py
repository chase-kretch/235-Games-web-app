from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime, ForeignKey, Text, Float
)
from sqlalchemy.orm import mapper, relationship

from games.domainmodel.model import User, Publisher, Game, Wishlist, Genre, Review

metadata = MetaData()

publishers_table = Table(
    'publishers', metadata,
    Column('name', String(255), nullable=True),
    Column('publisher_id', Integer, primary_key=True)# nullable=False, unique=True)
)

games_table = Table(
    'games', metadata,
    Column('game_id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('price', Float, nullable=False),
    Column('release_date', String(50), nullable=False),
    Column('game_description', String(255), nullable=True),
    Column('game_image_url', String(255), nullable=True),
    Column('game_website_url', String(255), nullable=True),
    Column('languages', String(255), nullable=True),
    Column('publisher_name', ForeignKey('publishers.name')),
    Column('genres', ForeignKey('genres.genre_id')),
)

genres_table = Table(
    'genres', metadata,
    # For genre again we only have name.
    Column('genre_id', Integer, primary_key = True, autoincrement=True),
    Column('genre_name', String(64), nullable=False)
)

game_genres_table = Table(
    'game_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('genre_id', ForeignKey('genres.genre_id'))
)

users_table = Table(
    'users', metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(20), nullable=False, unique=True),
    Column('password', String(20), nullable=False),)

reviews_table = Table(
    'reviews', metadata,
    Column('review_id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('comment', String(255), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('user_id', ForeignKey('users.user_id'))

)

user_favourite_games_table = Table(
    'user_favourite_games', metadata,
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('game_id', Integer, ForeignKey('games.game_id'))
)


def map_model_to_tables():
    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name,
    })

    mapper(Game, games_table, properties={
        '_Game__game_id': games_table.c.game_id,
        '_Game__game_title': games_table.c.title,
        '_Game__price': games_table.c.price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.game_description,
        '_Game__image_url': games_table.c.game_image_url,
        '_Game__website_url': games_table.c.game_website_url,
        # '_Game__languages': games_table.c.languages,
        '_Game__publisher': relationship(Publisher),
        '_Game__genres': relationship(Genre, secondary=game_genres_table),
        '_Game__reviews': relationship(Review, back_populates='_Review__game'),
        '_Game__favourite_users': relationship(User, secondary=user_favourite_games_table,
                                               back_populates='_User__favourite_games')

    })

    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,
    })
    mapper(User, users_table, properties={
        '_User__user_id': users_table.c.user_id,
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(Review, back_populates='_Review__user'),
        '_User__favourite_games': relationship(Game, secondary=user_favourite_games_table,
                                               back_populates='_Game__favourite_users')
    })
    mapper(Review, reviews_table, properties={
        '_Review__game': relationship(Game, back_populates='_Game__reviews'),
        '_Review__comment': reviews_table.c.comment,
        '_Review__rating': reviews_table.c.rating,
        '_Review__user': relationship(User, back_populates='_User__reviews')
    })
