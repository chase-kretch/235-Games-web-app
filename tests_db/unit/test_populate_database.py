from sqlalchemy import select, inspect

from games.adapters.orm import (metadata)


"""
This file is for unit testing of populate repository
Type 'python -m pytest' without quotation mark in terminal to test everything
Type 'python -m pytest tests_db' without quotation mark in terminal to test functionality related with database
"""


def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    # Look at here or DB browser if you want to know what table is in which index
    assert inspector.get_table_names() == ['game_genres', 'games', 'genres', 'publishers', 'reviews', 'user_favourite_games', 'users']

def test_database_populate_select_all_users(database_engine):
    inspector = inspect(database_engine)
    users_table = inspector.get_table_names()[-1]
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[users_table]])
        result = connection.execute(select_statement)
        all_users = []
        for row in result:
            all_users.append(row['username'])
        # We have one preloaded user
        assert all_users == ['admin']

def test_database_populate_select_games(database_engine):
    inspector = inspect(database_engine)
    games_table = inspector.get_table_names()[1]
    with (database_engine.connect() as connection):
        select_statement = select([metadata.tables[games_table]])
        result = connection.execute(select_statement)
        first_five_games = {'id':[], 'title':[]}
        count = 0
        for row in result:
            if count >= 5:
                break
            first_five_games['id'].append(row['game_id'])
            first_five_games['title'].append(row['title'])
            count += 1
        assert first_five_games['id'] == [3010, 7940, 11370, 12140, 12460]
        assert first_five_games['title'] == ["Xpand Rally", "Call of Duty® 4: Modern Warfare®", \
                                             "Nikopol: Secrets of the Immortals", "Max Payne", "BC Kings"]

def test_database_populate_select_genres(database_engine):
    inspector = inspect(database_engine)
    genres_table = inspector.get_table_names()[2]
    with (database_engine.connect() as connection):
        select_statement = select([metadata.tables[genres_table]])
        result = connection.execute(select_statement)
        first_five_unique_genres = []
        count = 0
        for row in result:
            if count >= 5:
                break
            if row['genre_name'] not in first_five_unique_genres:
                first_five_unique_genres.append(row['genre_name'])
                count += 1
        assert first_five_unique_genres == ['Action', 'Adventure', 'Casual', 'Indie', 'Early Access']

def test_database_populate_select_all_publishers(database_engine):
    inspector = inspect(database_engine)
    publishers_table = inspector.get_table_names()[3]
    with (database_engine.connect() as connection):
        select_statement = select([metadata.tables[publishers_table]])
        result = connection.execute(select_statement)
        first_five_publishers = []
        count = 0
        for row in result:
            if count >= 5:
                break
            if row['name'] not in first_five_publishers:
                first_five_publishers.append(row['name'])
                count += 1
        assert first_five_publishers == ['Activision', 'Beep Games, Inc.', 'Buka Entertainment', 'D3PUBLISHER', 'I-Illusions']


"""
I haven't done test for reviews and wishlist as we don't have preloaded data.
"""