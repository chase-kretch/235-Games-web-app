from pathlib import Path
import os
from games.adapters.repository import AbstractRepository
from games.adapters.datareader.csvdatareader import GameFileCSVReader, UserFileCSVReader


def add_games(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(dir_name, "data/games.csv")  # Get the repository and set that as the filename of the csv file we want to read
    reader = GameFileCSVReader(file_name)
    reader.read_csv_file()
    games = reader.dataset_of_games  # Generate all the games into a dataset
    for game in games:
        repo.add_game(game)  # Add each game to the repo from the csv file


def load_users(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(dir_name, "data/users.csv")
    reader = UserFileCSVReader(file_name)
    reader.read_csv_file()
    users = reader.dataset_of_users
    for user in users:
        repo.add_user(user)


def populate(repo: AbstractRepository):
    add_games(repo)
    load_users(repo)