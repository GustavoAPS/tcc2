import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from dotenv import load_dotenv
from flask_migrate import Migrate
from functools import wraps
from models import User, Game, db
from DadosEstaticos import default_user_prefs

load_dotenv()

app = Flask(__name__)

# config database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db.init_app(app)

migrate = Migrate(app, db)

# move to another file
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to be logged in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def calculate_weight(game: Game, user: User):
    recomendation_weight = 0
    categories = game.get_categories()
    user_prefs_dict = user.get_prefs()

    for category in categories:
        recomendation_weight += user_prefs_dict[category]

    return recomendation_weight


@app.route('/')
def index():
    games = Game.query.all()

    if 'user_id' in session:
        user = db.get_or_404(User, session['user_id']) 
        games_with_weights = [(game, calculate_weight(game, user)) for game in games]
        games_with_weights.sort(key=lambda x: x[1], reverse=True)
        return render_template('index.html', games_with_weights=games_with_weights)

    else:
        games_with_weights = [(game,0) for game in games]
        return render_template('index.html', games_with_weights=games_with_weights)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(name=username).first_or_404()

    if user and user.check_password(password):
        session['user_id'] = user.id
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201


@app.route("/users/<int:id>", methods=['GET'])
@login_required
def user_by_id(id):
    user = db.get_or_404(User, id)
    return render_template('view_user.html', user=user)


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.get_or_404(User, id)
    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
    db.session.commit()
    return jsonify({'message': 'User updated'}), 200


@app.route('/users/<int:id>', methods=['POST'])
def delete_user(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/create_game', methods=['GET', 'POST'])
def create_game():
    if request.method == 'POST':
        form_name = request.form.get('name')

        form_categories = request.form.getlist('category')

        flash('Jogo criado com sucesso!', 'success')

        new_game = Game(name=form_name)
        new_game.set_categories(form_categories)
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('index'))
       
    return render_template('register_game.html')


@app.route("/game/<int:id>", methods=['GET'])
def game_by_id(id):
    game = db.get_or_404(Game, id)
    return render_template('view_game.html', game=game)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        genres = request.form.getlist('genres')
        play_time = request.form.getlist('play-time')
        game_style = request.form.getlist('game-style')
        interest_level = request.form.getlist('interest-level')

        new_user_prefs = default_user_prefs  # get the defaul user prefs dict

        if 'music' in genres:
            new_user_prefs["musical"] += 3
            new_user_prefs["sensorial"] += 2
            new_user_prefs["meditation"] += 1

        if 'story' in genres:
            new_user_prefs["narrative"] += 3
            new_user_prefs["adventure"] += 2
            new_user_prefs["rpg"] += 2

        if 'puzzle' in genres:
            new_user_prefs["puzzle"] += 3
            new_user_prefs["strategy"] += 2
            new_user_prefs["simulation"] += 1

        if 'art' in genres:
            new_user_prefs["painting"] += 3
            new_user_prefs["sensorial"] += 2
            new_user_prefs["meditation"] += 1

        if 'short-time' in play_time:
            new_user_prefs["arcade"] += 3
            new_user_prefs["casual"] += 2
            new_user_prefs["idle"] += 1

        if 'medium-time' in play_time:
            new_user_prefs["virtual-version"] += 3
            new_user_prefs["casual"] += 2

        if 'long-time' in play_time:
            new_user_prefs["simulation"] += 3
            new_user_prefs["strategy"] += 2
            new_user_prefs["rpg"] += 2
            new_user_prefs["adventure"] += 1

        if 'co-op' in game_style:
            new_user_prefs["co-op"] += 3
            new_user_prefs["social"] += 2

        if 'competitive' in game_style:
            new_user_prefs["competitive"] += 3
            new_user_prefs["strategy"] += 2

        if 'open-world' in game_style:
            new_user_prefs["open-world"] += 3
            new_user_prefs["adventure"] += 2

        if 'narrative' in game_style:
            new_user_prefs["narrative"] += 3
            new_user_prefs["adventure"] += 2
            new_user_prefs["rpg"] += 1

        if 'social' in game_style:
            new_user_prefs["social"] += 3
            new_user_prefs["co-op"] += 2

        if 'sports' in interest_level:
            new_user_prefs["sports"] += 3

        if 'somewhat' in interest_level:
            new_user_prefs["sports"] += 2

        if 'not-interested' in interest_level:
            new_user_prefs["sports"] -= 3

        if not (username and password and confirm_password):
            flash('Todos os campos são obrigatórios!', 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('register'))

        string_confirmacao = (f"Genres: {', '.join(genres)}") + (f"Play time: {', '.join(play_time)}")

        flash(string_confirmacao, 'success')

        new_user = User(name=username)
        new_user.set_password(password)
        new_user.set_prefs(new_user_prefs)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('register_user.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')
