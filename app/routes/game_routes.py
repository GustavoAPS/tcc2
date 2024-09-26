from flask import (
    Blueprint, request, session,
    redirect, url_for, render_template, flash
)
from app.models import Game, Comment, db

game_bp = Blueprint('game', __name__)


@game_bp.route('/create_game', methods=['GET', 'POST'])
def create_game():
    if request.method == 'POST':
        form_name = request.form.get('name')

        form_categories = request.form.getlist('category')

        flash('Jogo criado com sucesso!', 'success')

        new_game = Game(name=form_name)
        new_game.set_categories(form_categories)
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('user.index'))     
    return render_template('register_game.html')


@game_bp.route('/create_comment/<int:game_id>', methods=['POST'])
def create_comment(game_id):

    text = request.form['text']
    rating = int(request.form['rating'])

    if 'user_id' in session:
        new_comment = Comment(user_id=session['user_id'],
                              game_id=game_id,
                              text=text,
                              rating=rating)

    db.session.add(new_comment)
    db.session.commit()

    flash('Comment created successfully!', 'success')

    return redirect(url_for('game.game_by_id', id=game_id))


@game_bp.route("/game/<int:id>", methods=['GET'])
def game_by_id(id):
    game = db.get_or_404(Game, id)

    # Query to get all comments associated with the game_id
    comments = Comment.query.filter_by(game_id=game.id).all()

    return render_template('view_game.html', game=game, comments=comments)
