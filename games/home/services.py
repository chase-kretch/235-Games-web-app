from games.adapters.memory_repository import AbstractRepository


def get_unique_genres(repo: AbstractRepository):
    games = repo.get_games()
    genres = []
    for game in games:
        for genre in game.genres:
            if genre not in genres:
                genres.append(genre)
    genres.sort()
    return genres


def get_games_by_price(repo: AbstractRepository, lower_price, upper_price=None):
    games = repo.get_games()
    if upper_price is None:
        games_to_show = [game for game in games if lower_price < game.price]
    else:
        games_to_show = [game for game in games if lower_price < game.price <= upper_price]
    return sorted(games_to_show, key=lambda game: (game.price, game.title))
