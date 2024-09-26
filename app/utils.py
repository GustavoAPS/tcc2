from functools import wraps
from flask import session, flash, redirect, url_for
from app.models import Game, User


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to be logged in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def calculate_weight(game: Game, user: User):
    recommendation_weight = 0
    categories = game.get_categories()
    user_prefs_dict = user.get_prefs()

    for category in categories:
        recommendation_weight += user_prefs_dict.get(category, 0)

    return recommendation_weight