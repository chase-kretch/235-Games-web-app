from flask import Flask, render_template, Blueprint, request, url_for, redirect
import games.adapters.repository as repo
from games.browse import services
from games.home.services import get_unique_genres

### Browse Blueprint

browse_blueprint = Blueprint('games_bp', __name__)
"""Redundant Games Blueprint"""
# @browse_blueprint.route('/games', methods=['GET'])
# def browse_games():
#     num_games = services.get_number_of_games(repo.repo_instance)
#     all_games = services.get_games(repo.repo_instance)
#     return render_template('games/games.html',  # At the moment, since we dont have templates I've only included num games and games as parameters.
#                            num_games = num_games,
#                            games = all_games)
#                             # Room for templates such as title, heading, etc.


@browse_blueprint.route('/games', methods=['GET'])
def games():
    # I will enable this later
    # number_of_games_in_page = request.args.get('num_games')
    number_of_games_in_page = 5
    target_id = request.args.get('id')
    num_games = services.get_number_of_games(repo.repo_instance)
    # If there is no games to show, redirect to home page
    if num_games <= 0:
        return redirect(url_for('home_bp.home'))
    first_game = services.get_first_game(repo.repo_instance)
    last_game = services.get_last_game(repo.repo_instance)
    if target_id is None:
        target_id = first_game.game_id
    else:
        # Convert query string to int type for processing
        target_id = int(target_id)
        print(target_id)
    games_to_show, previous_id, next_id = services.get_games_by_id(target_id, number_of_games_in_page, repo.repo_instance, "all")

    # if games_to_show is empty, it means query value is wrong, so set target id to id of first game
    if len(games_to_show) <= 0:
        target_id = first_game.game_id
        games_to_show, previous_id, next_id = services.get_games_by_id(target_id, number_of_games_in_page,
                                                                       repo.repo_instance)

    first_page_url = None
    previous_page_url = None
    next_page_url = None
    last_page_url = None

    if previous_id is not None:
        first_page_url = url_for('games_bp.games', id=first_game.game_id)
        previous_page_url = url_for('games_bp.games', id=previous_id)
    if next_id is not None:
        next_page_url = url_for('games_bp.games', id=next_id)
        last_page_url = url_for('games_bp.games', id=last_game.game_id)

    return render_template(
        'games/games_by_id.html',
        num_games=num_games,
        games=games_to_show,
        previous_page_url=previous_page_url,
        next_page_url=next_page_url,
        previous_id=previous_id,
        next_id=next_id,
        first_page_url=first_page_url,
        first_id=first_game.game_id,
        last_page_url=last_page_url,
        last_id=last_game.game_id,
        unique_genres=get_unique_genres(repo.repo_instance)
    )


@browse_blueprint.route('/genre/<genre_name>')
def genre_games(genre_name):
    number_of_games_in_page = 5
    target_id = request.args.get('id')

    num_games = services.get_number_of_genre_games(repo.repo_instance, genre_name)
    first_game = services.get_first_genre_game(repo.repo_instance, genre_name)
    last_game = services.get_last_genre_game(repo.repo_instance, genre_name)

    if target_id is None:
        target_id = first_game.game_id
    else:
        target_id = int(target_id)

    # Retrieve games associated with the selected genre and ID
    games_to_show, previous_id, next_id = services.get_games_by_id(
        target_id, number_of_games_in_page, repo.repo_instance, genre_name
    )
    first_page_url = None
    previous_page_url = None
    next_page_url = None
    last_page_url = None

    if previous_id is not None:
        first_page_url = url_for('games_bp.genre_games', genre_name=genre_name, id=first_game.game_id)
        previous_page_url = url_for('games_bp.genre_games', genre_name=genre_name, id=previous_id)
    if next_id is not None:
        next_page_url = url_for('games_bp.genre_games', genre_name=genre_name, id=next_id)
        last_page_url = url_for('games_bp.genre_games', genre_name=genre_name, id=last_game.game_id)

    return render_template(
        'games/games_by_genre.html',
        genre=genre_name,
        num_games=num_games,
        games=games_to_show,
        previous_page_url=previous_page_url,
        next_page_url=next_page_url,
        previous_id=previous_id,
        next_id=next_id,
        first_page_url=first_page_url,
        first_id=first_game.game_id,
        last_page_url=last_page_url,
        last_id=last_game.game_id,
        unique_genres=get_unique_genres(repo.repo_instance)
    )


@browse_blueprint.route('/search', methods=['GET'])
def search_games():
    search_query = request.args.get('query')
    search_criteria = request.args.get('criteria')
    search_genre = request.args.get('genre')

    if not search_query or not search_criteria:  # Check if user entered anything
        return redirect(url_for('games_bp.games'))

    number_of_games_in_page = 5
    filtered_games = services.get_games_with_search(repo.repo_instance, search_query, search_criteria, search_genre)
    num_games = len(filtered_games)

    if not filtered_games:
        return render_template(
            'games/games_search.html',
            query=search_query,
            criteria=search_criteria,
            genre=search_genre,
            games=[],
            previous_page_url=None,
            next_page_url=None,
            first_page_url=None,
            last_page_url=None,
            first_id=None,
            previous_id=None,
            next_id=None,
            last_id=None,
            num_games=0,
            unique_genres=get_unique_genres(repo.repo_instance)
        )

    target_id = request.args.get('id')
    if filtered_games:
        first_game = filtered_games[0]
        first_id = first_game.game_id
        last_game = filtered_games[-1]
        last_id = last_game.game_id
    else:
        first_game, last_game = None, None

    if target_id is None:
        if first_game is None:
            filtered_games = []  # No games to show
            first_game = None
            first_id = None
            last_game = None
            last_id = None
        else:
            target_id = first_game.game_id
    else:
        target_id = int(target_id)

    games_to_show, previous_id, next_id = services.get_games_by_id(
        target_id, number_of_games_in_page, repo.repo_instance, "all", filtered_games)

    first_page_url = None
    previous_page_url = None
    next_page_url = None
    last_page_url = None

    if previous_id is not None:
        first_page_url = url_for('games_bp.search_games', id=first_game.game_id,
                                 query=search_query, criteria=search_criteria)
        previous_page_url = url_for('games_bp.search_games', id=previous_id,
                                    query=search_query, criteria=search_criteria)
    if next_id is not None:
        next_page_url = url_for('games_bp.search_games', id=next_id,
                                query=search_query, criteria=search_criteria)
        last_page_url = url_for('games_bp.search_games', id=last_game.game_id,
                                query=search_query, criteria=search_criteria)

    return render_template(
        'games/games_search.html',
        query=search_query,
        criteria=search_criteria,
        genre=search_genre,
        games=games_to_show,
        previous_page_url=previous_page_url,
        next_page_url=next_page_url,
        first_page_url=first_page_url,
        last_page_url=last_page_url,
        first_id=first_id,
        previous_id=previous_id,
        next_id=next_id,
        last_id=last_id,
        num_games=num_games,
        unique_genres=get_unique_genres(repo.repo_instance)
    )

