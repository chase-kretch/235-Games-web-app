import csv
import os

from games.domainmodel.model import Genre, Game, Publisher, User


class GameFileCSVReader:
    def __init__(self, filename):
        self.__filename = filename
        self.__dataset_of_games = []
        self.__dataset_of_publishers = set()
        self.__dataset_of_genres = set()

    def read_csv_file(self):
        if not os.path.exists(self.__filename):
            print(f"path {self.__filename} does not exist!")
            return
        with open(self.__filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    game_id = int(row["AppID"])
                    title = row["Name"]
                    game = Game(game_id, title)
                    game.release_date = row["Release date"]
                    game.price = float(row["Price"])
                    game.description = row["About the game"]
                    game.image_url = row["Header image"]
                    publisher = Publisher(row["Publishers"])
                    self.__dataset_of_publishers.add(publisher)
                    game.publisher = publisher
                    game.review = str(row["Reviews"])

                    """languages_str = row["Supported languages"]
                    languages_str = languages_str.replace('[', '').replace(']', '').replace("'", '')
                    languages_list = [language.strip() for language in languages_str.split(",")]
                    game.languages = languages_list"""

                    genre_names = row["Genres"].split(",")
                    for genre_name in genre_names:
                        genre = Genre(genre_name.strip())
                        self.__dataset_of_genres.add(genre)
                        game.add_genre(genre)

                    self.__dataset_of_games.append(game)

                except ValueError as e:
                    print(f"Skipping row due to invalid data: {e}")
                except KeyError as e:
                    print(f"Skipping row due to missing key: {e}")

    def get_unique_games_count(self):
        return len(self.__dataset_of_games)

    def get_unique_genres_count(self):
        return len(self.__dataset_of_genres)

    def get_unique_publishers_count(self):
        return len(self.__dataset_of_publishers)

    @property
    def dataset_of_games(self) -> list:
        return self.__dataset_of_games

    @property
    def dataset_of_publishers(self) -> set:
        return self.__dataset_of_publishers

    @property
    def dataset_of_genres(self) -> set:
        return self.__dataset_of_genres

class UserFileCSVReader:
    def __init__(self, filename):
        self._filename = filename
        self._dataset_of_users = []

    def read_csv_file(self):
        if not os.path.exists(self._filename):
            print(f"path {self._filename} does not exist!")
            return
        with open(self._filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    user_id = int(row["ID"])
                    username = row["Username"]
                    password = row["Password"]
                    user = User(username, password)
                    # user.reviews = xx
                    # user.fav_games = xx
                    self._dataset_of_users.append(user)
                except ValueError as e:
                    print(f"Skipping row due to invalid data: {e}")
                except KeyError as e:
                    print(f"Skipping row due to missing key: {e}")

    @property
    def dataset_of_users(self) -> list:
        return self._dataset_of_users
