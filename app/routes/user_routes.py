from flask import (
    Blueprint, request, session, jsonify,
    redirect, url_for, render_template, flash
)
from app.models import User, Game, StressRecord, db
from app.utils import login_required, calculate_weight
from datetime import datetime, timezone
from DadosEstaticos import default_user_prefs

user_bp = Blueprint('user', __name__)


@user_bp.route('/')
def index():
    games = Game.query.all()

    if 'user_id' in session:
        user = db.get_or_404(User, session['user_id'])
        games_with_weights = [
            (game, calculate_weight(game, user))
            for game in games
            ]
        games_with_weights.sort(key=lambda x: x[1], reverse=True)

        latest_stress_record = user.get_latest_stress_record()
        stress_level = latest_stress_record.stress_level if latest_stress_record else 0

        return render_template('index.html',
                               games_with_weights=games_with_weights,
                               user=user,
                               stress_level=stress_level)

    else:
        games_with_weights = [(game, 0) for game in games]
        return render_template('index.html',
                               games_with_weights=games_with_weights)


@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201


@user_bp.route("/users/<int:id>", methods=['GET'])
@login_required
def user_by_id(id):
    user = db.get_or_404(User, id)
    return render_template('view_user.html', user=user)


@user_bp.route("/profile", methods=['GET'])
def view_user_profile():
    if 'user_id' in session:

        user = db.get_or_404(User, session['user_id'])
        stress_data = (StressRecord.query
                       .filter_by(user_id=user.id)
                       .order_by(StressRecord.date)
                       .all())
        labels = [record.date.strftime('%Y-%m-%d') for record in stress_data]
        data = [record.stress_level for record in stress_data]
        latest_stress_record = user.get_latest_stress_record()
        stress_level = latest_stress_record.stress_level if latest_stress_record else 0
        return render_template('view_user.html',
                               user=user,
                               data=data,
                               labels=labels,
                               stress_level=stress_level)
    return redirect(url_for('user.index'))


@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return render_template('user_list.html', users=users)


@user_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.get_or_404(User, id)
    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
    db.session.commit()
    return jsonify({'message': 'User updated'}), 200


@user_bp.route('/users/<int:id>', methods=['POST'])
def delete_user(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    users = User.query.all()
    return render_template('user_list.html', users=users)


@login_required
@user_bp.route('/stress_record', methods=['GET', 'POST'])
def create_stress_record():
    if request.method == 'POST':
        q1 = int(request.form.get('question1'))
        q2 = int(request.form.get('question2'))
        q3 = int(request.form.get('question3'))
        q4 = int(request.form.get('question4'))
        q5 = int(request.form.get('question5'))
        q6 = int(request.form.get('question6'))
        q7 = int(request.form.get('question7'))
        q8 = int(request.form.get('question8'))
        q9 = int(request.form.get('question9'))
        q10 = int(request.form.get('question10'))

        # Os itens 4, 5, 7 e 8 são positivos e por esta razão devem ter a
        # pontuação revertida
        # Ex: 0 = 4, 1 = 3, 2 = 2, 3 = 1 e 4 = 0
        total_stress = (
            q1 + q2 + q3 + (4 - q4) +
            (4 - q5) + q6 + (4 - q7) +
            (4 - q8) + q9 + q10
        )

        print(f"Stress total {total_stress}", flush=True)

        if 'user_id' in session:
            usr_id = session['user_id']

        new_stress_record = StressRecord(user_id=usr_id,
                                         stress_level=total_stress,
                                         date=datetime.now(timezone.utc))
        db.session.add(new_stress_record)
        db.session.commit()

        return redirect(url_for('user.index'))
    return render_template('register_stress.html')


@user_bp.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('user.register'))

        if password != confirm_password:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('user.register'))

        # Check if a user with the same username already exists
        existing_user = User.query.filter_by(name=username).first()
        if existing_user:
            flash('Este nome de usuário já está em uso.', 'danger')
            return redirect(url_for('user.register'))

        new_user = User(name=username)
        new_user.set_password(password)
        new_user.set_prefs(new_user_prefs)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        session['username'] = new_user.name

        return redirect(url_for('user.index'))

    return render_template('register_user.html')
