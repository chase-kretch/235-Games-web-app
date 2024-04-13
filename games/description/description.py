from flask import Blueprint, render_template, session, redirect, url_for, request
from games.description import services
import games.adapters.repository as repo
from games.home.services import get_unique_genres
from games.wishlist.services import get_user_for_wishlist
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from games.authentication.authentication import login_required
description_blueprint = Blueprint('description_bp', __name__)


@description_blueprint.route('/description/<int:game_id>', methods=['GET'])
def description(game_id):
    game = services.get_game_id(game_id, repo.repo_instance)
    # game['reviews'] = services.format_reviews(game['reviews'])
    if 'username' in session:
        username = session['username']
        user = get_user_for_wishlist(username, repo.repo_instance)
        fav = repo.repo_instance.get_wishlist(username)
        print(fav)
        game_in_wishlist = any(game.game_id == game_id for game in fav)
        print(game_id)
        print(game_in_wishlist)
        can_review = services.validity_of_review(game_id, username, repo.repo_instance)
    else:
        user = None
        game_in_wishlist = None
        can_review = True
    average_rating = services.average_rating(game_id, repo.repo_instance)
    return render_template('gameDescription/gameDescription.html',
                           game=game,
                           unique_genres=get_unique_genres(repo.repo_instance),
                           can_review=can_review,
                           user=user,
                           game_in_wishlist=game_in_wishlist,
                           average_rating = average_rating
                           )


@description_blueprint.route('/review/<int:game_id>', methods=['GET', 'POST'])
@login_required
def review_game(game_id):
    username = session['username']

    form = ReviewForm()

    if form.validate_on_submit():
        game_id = int(form.game_id.data)
        services.add_review(game_id, form.review.data, form.rating.data, username, repo.repo_instance)

        game = services.get_game_id(game_id, repo.repo_instance)
        print(game['reviews'])
        return redirect(url_for('description_bp.description', game_id=game_id))

    if request.method == 'GET':

        form.game_id.data = game_id
    else:
        game_id = int(form.game_id.data)

    game = services.get_game_id(game_id, repo.repo_instance)
    return render_template(
        'gameDescription/review.html',
        game=game,
        form=form,
        title="Add a review",
        unique_genres=get_unique_genres(repo.repo_instance)
    )


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [DataRequired(),
                                      Length(min=4, message="Your comment is too short")
                                    ])
    choices = [(i, str(i)) for i in range(1, 6)]
    rating = SelectField('Select a rating: ', choices=choices, coerce=int, validators=[DataRequired()])
    game_id = HiddenField('Game id')
    submit = SubmitField('Submit')