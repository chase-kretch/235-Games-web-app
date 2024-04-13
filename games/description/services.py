from games.adapters.repository import AbstractRepository
import re
from games.domainmodel.model import Game, Review
from typing import Iterable
class NotLoggedInException(Exception):
    pass

class NonExistentGameException(Exception):
    pass


def get_game_id(game_id, repo: AbstractRepository): # Gets the game from the repo via the game_id
    game = repo.get_game_id(game_id)
    if game is not None:
        return {'game_id': game.game_id,
                'title': game.title,
                'url': game.image_url,
                'price': game.price,
                'release_date': game.release_date,
                'description': game.description,
                'publisher': game.publisher,
                'genres': ', '.join(genre.genre_name for genre in game.genres),
                'reviews': game.reviews}
    return None


def format_reviews(reviews):
    # Looks for patterns like: "Review text" Source
    pattern = r'“(.*?)”\s*([-–—]?\s*.*?)(?=\s*“|$)'
    formatted_reviews = re.findall(pattern, reviews)
    # If the pattern is not found, return the original review as a list
    if not formatted_reviews:
        return [reviews]
    return formatted_reviews


def add_review(game_id: int, review_text: str, rating: int, username, repo: AbstractRepository):
    game = repo.get_game_id(game_id)
    if game is None:
        raise NonExistentGameException

    user = repo.get_user(username)
    if user is None:
        raise NotLoggedInException

    review = Review(user, game, rating, review_text)
    repo.add_review(review)

def review_to_dict(review):
    review_dict = {
        'username': review.user.username,
        'game': review.game,
        'review_text': review.comment,
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


def validity_of_review(game_id, username, repo: AbstractRepository):
    game = repo.get_game_id(game_id)
    if game is None:
        raise ValueError("Game not found for the provided game_id")
    for review in game.reviews:
        if username == review.user.username:
            return False
    return True

def average_rating(game_id, repo):

    game = repo.get_game_id(game_id)
    review_list = game.reviews
    total = len(review_list)
    rating_sum = 0
    if total == 0:
        return "No reviews"
    for review in review_list:
        rating = review.rating
        rating_sum += rating
    return round(rating_sum / total, 1)

