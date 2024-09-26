from flask import Blueprint, request, session, redirect, url_for
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(name=username).first_or_404()

    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.name
        return redirect(url_for('user.index'))
    else:
        return redirect(url_for('user.index'))


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('user.index'))
