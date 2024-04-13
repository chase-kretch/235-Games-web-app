from flask import Blueprint, render_template, session, redirect, url_for, request
import games.wishlist.services as services
import games.adapters.repository as repo
from games.authentication.authentication import login_required
from games.home.services import get_unique_genres

wishlist_blueprint = Blueprint('wishlist_bp', __name__, url_prefix='/wishlist')


@wishlist_blueprint.route('/add/<int:game_id>', methods=['POST'])
def add_to_wishlist(game_id):
    if 'username' not in session:
        return redirect(url_for('auth_bp.login'))  # Redirect to login if the user is not authenticated
    username = session['username']
    repo.repo_instance.add_game_to_wishlist(username, game_id)
    return redirect(url_for('profile_bp.profile'))


@wishlist_blueprint.route('/remove/<int:game_id>', methods=['POST'])
def remove_from_wishlist(game_id):
    if 'username' not in session:
        return redirect(url_for('auth_bp.login'))  # Redirect to login if the user is not authenticated
    username = session['username']
    repo.repo_instance.remove_game_from_wishlist(username, game_id)
    return redirect(url_for('profile_bp.profile'))


@wishlist_blueprint.route('/toggle_wishlist', methods=['POST'])
@login_required
def toggle_wishlist():
    game_id = int(request.form['game_id'])
    action = request.form['action']
    username = session['username']
    user = services.get_user_for_wishlist(username, repo.repo_instance)
    game = repo.repo_instance.get_game_id(game_id)
    fav = repo.repo_instance.get_wishlist(username)
    if user is not None and game is not None:
        if action == 'add':
            if game not in fav:
                repo.repo_instance.add_game_to_wishlist(username, game_id)
        elif action == 'remove':
            if game in fav:
                repo.repo_instance.remove_game_from_wishlist(username, game_id)
    return redirect(url_for('description_bp.description', game_id=game_id, user=user))

@wishlist_blueprint.route('/', methods=['GET'])
@login_required
def wishlist():
    username = session['username']
    fav = repo.repo_instance.get_wishlist(username)
    num_of_favgames = len(fav)
    games = [game for game in fav]
    return render_template("userProfile/profileWishlist.html",
                           username=username,
                           wishlist=games,
                           num_of_favgames=num_of_favgames,
                           unique_genres=get_unique_genres(repo.repo_instance)  # for sidebar
                           )