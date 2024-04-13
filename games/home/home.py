from flask import Blueprint, render_template
from games.home import services
import games.adapters.repository as repo

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/')
def home():
    unique_genres = services.get_unique_genres(repo.repo_instance)
    free_to_play_games = services.get_games_by_price(repo.repo_instance, -1, 0)
    under_5_games = services.get_games_by_price(repo.repo_instance, 0, 5)
    between_5_and_10_games = services.get_games_by_price(repo.repo_instance, 5, 10)
    between_10_and_20_games = services.get_games_by_price(repo.repo_instance, 10, 20)
    above_20_games = services.get_games_by_price(repo.repo_instance, 20)
    return render_template('home/home.html',
                           unique_genres=unique_genres,
                           free_to_play_games=free_to_play_games,
                           under_5_games=under_5_games,
                           between_5_and_10_games=between_5_and_10_games,
                           between_10_and_20_games=between_10_and_20_games,
                           above_20_games=above_20_games)
