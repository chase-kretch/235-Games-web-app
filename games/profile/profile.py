from flask import Blueprint, render_template, session, redirect, url_for, request
import games.authentication.services as services
import games.profile.services as user_services
import games.adapters.repository as repo
from games.authentication.authentication import login_required
from games.home.services import get_unique_genres

profile_blueprint = Blueprint('profile_bp', __name__, url_prefix='/profile')


@profile_blueprint.route('/', methods=['GET'])
@login_required
def profile():
    username = session['username']
    user = user_services.get_user(username, repo.repo_instance)
    reviews = user.reviews
    num_of_reviews = len(reviews)
    fav = repo.repo_instance.get_wishlist(username)
    num_of_favgames = len(fav)
    games = [game for game in fav]
    return render_template("userProfile/profile.html",
                           username=username,
                           reviews=reviews,
                           num_of_reviews=num_of_reviews,
                           wishlist=games,
                           num_of_favgames=num_of_favgames,
                           unique_genres=get_unique_genres(repo.repo_instance)  # for sidebar
                           )




@profile_blueprint.route('/reviews', methods=['GET'])
@login_required
def reviews():
    username = session['username']
    user = user_services.get_user(username, repo.repo_instance)
    reviews = user.reviews
    num_of_reviews = len(reviews)
    return render_template("userProfile/profileReviews.html",
                           username=username,
                           reviews=reviews,
                           num_of_reviews=num_of_reviews,
                           unique_genres=get_unique_genres(repo.repo_instance)  # for sidebar
                           )





@profile_blueprint.route('/change_username', methods=['GET', 'POST'])
def change_username():
    pass

@profile_blueprint.route('/change_password', methods=['GET'])
@login_required
def change_password():
    return redirect(url_for('auth_bp.change_password'))


@profile_blueprint.route('/delete_account', methods=['GET'])
@login_required
def delete_account():
    confirm = request.args.get('confirm')
    if confirm == "True":
        user_services.delete_account(session['username'], repo.repo_instance)
        return redirect(url_for('auth_bp.logout'))
    return render_template("userProfile/profileDeleteAccount.html")
