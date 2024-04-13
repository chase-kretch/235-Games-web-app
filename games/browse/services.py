from flask import url_for
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game  # I dont think this is necessary but I will keep it incase it causes an error.


# import the repository that contains the read CSV file and also the Game module from the model file.


def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()


def get_games(repo: AbstractRepository):
    games = repo.get_games()
    game_dicts = []
    for game in games:
        temp = {'game_id': game.game_id, 'title': game.title, 'game_url': game.release_date}
        game_dicts.append(temp)

    return game_dicts


def get_first_game(repo: AbstractRepository):
    games = repo.get_games()
    return sorted(games, key=lambda x: x.title)[0]


def get_last_game(repo: AbstractRepository):
    games = repo.get_games()
    return sorted(games, key=lambda x: x.title)[-1]


def get_games_by_id(id: int, number_of_games_in_page: int, repo: AbstractRepository, genre_name, filtered_games=None):
    if filtered_games:  # Check if using default game library or filtered games (for search games)
        games = filtered_games
    else:
        games = repo.get_games()

    if genre_name != "all":  # Check if using default game library or games based on a specific genre
        games = [game for game in games if any(genre.genre_name == genre_name for genre in game.genres)]

    games = sorted(games, key=lambda x: x.title)

    games_to_show = []
    index = 0
    previous_id = None
    next_id = None
    if len(games) > 0:
        # Find index using id of certain game
        for i in range(len(games)):
            if games[i].game_id == id:
                if i == 0:
                    pass
                elif i > number_of_games_in_page:
                    previous_id = games[i - number_of_games_in_page].game_id
                else:
                    previous_id = games[0].game_id
                index = i
                if i < len(games) - number_of_games_in_page:
                    next_id = games[i + number_of_games_in_page].game_id
                break
        # Insert games in games_to_show until index is valid
        print(index)
        for i in range(index, index + number_of_games_in_page):
            if i < len(games):
                game = games[i]
                games_to_show.append({'game_id': game.game_id, 'title': game.title, 'game_url': game.release_date,
                                      'game_img': game.image_url})
    return games_to_show, previous_id, next_id


def get_games_for_genre(repo: AbstractRepository, genre_name):
    games = repo.get_games()
    games = sorted(games, key=lambda x: x.title)
    return [game for game in games if any(genre.genre_name == genre_name for genre in game.genres)]


def get_number_of_genre_games(repo: AbstractRepository, genre_name):
    games_for_genre = get_games_for_genre(repo, genre_name)
    return len(games_for_genre)


def get_first_genre_game(repo: AbstractRepository, genre_name):
    games_for_genre = get_games_for_genre(repo, genre_name)
    if games_for_genre:
        return games_for_genre[0]
    return None


def get_last_genre_game(repo: AbstractRepository, genre_name):
    games_for_genre = get_games_for_genre(repo, genre_name)
    if games_for_genre:
        return games_for_genre[-1]
    return None


def get_games_with_search(repo: AbstractRepository, search_query, search_criteria, genre=None, language=None):
    games = repo.get_games()

    if search_query and search_criteria:  # Check if user entered anything
        if search_criteria == 'title':
            filtered_games = [game for game in games if search_query.lower() in game.title.lower()]
        elif search_criteria == 'publisher':
            filtered_games = [game for game in games if search_query.lower() in game.publisher.publisher_name.lower()]
        else:
            filtered_games = [game for game in games if search_query.lower() in game.title.lower() or
                              search_query.lower() in game.publisher.publisher_name.lower()]
    else:
        filtered_games = []

    if genre and genre != "all":  # Check if user selected a specific genre
        filtered_games = [game for game in filtered_games if any(g.genre_name == genre for g in game.genres)]

    return sorted(filtered_games, key=lambda x: x.title)
