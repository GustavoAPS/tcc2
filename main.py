#import libraries
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

#load .env file, with the enviroment variables
load_dotenv()

#start flask app
app = Flask(__name__)

#config database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


# Define user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# Define game model
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return f'<User {self.name}>'



@app.route('/')
def index():
    return render_template('index.html')


#CRUD - Users

# Create
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201


# Read - Single
@app.route("/users/<int:id>", methods=['GET'])
def user_by_id(id):
    print('got into single user')
    user = db.get_or_404(User, id)
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email}])


# Read - All
@app.route('/users', methods=['GET'])
def get_users():
    print('got into all users')
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

# Update
# ------------------------------------------------------------ MISSING
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.get_or_404(User, id)
    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.name = data['email']
    db.session.commit()
    return jsonify({'message': 'User updated'}), 200

# Delete
# ------------------------------------------------------------ MISSING
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200


#CRUD - Games

# Create
# ------------------------------------------------------------ MISSING
# Read - Single
# ------------------------------------------------------------ MISSING
# Read - All
# ------------------------------------------------------------ MISSING
# Update 
# ------------------------------------------------------------ MISSING
# Delete
# ------------------------------------------------------------ MISSING

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']  

    # Teste de autentificação
    if email == 'test@example.com' and password == 'password':  
        flash('Login bem-sucedido!', 'success')
        print(f"Email: {email}")
        print(f"Senha: {password}")
        return redirect(url_for('index'))
    else:
        flash('Email ou senha inválidos.', 'warning')
        print(f"Email: {email}")
        print(f"Senha: {password}")
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        confirm_email = request.form.get('confirm_email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        anxiety = request.form.get('anxiety')
        competitiveness = request.form.get('competitiveness')

        genres = request.form.getlist('genres')
        activities = request.form.getlist('activities')
        motivations = request.form.getlist('motivations')

        # Validações
        if not (username and email and confirm_email and password and confirm_password):
            flash('Todos os campos são obrigatórios!', 'danger')
            return redirect(url_for('register'))

        if email != confirm_email:
            flash('Os e-mails não coincidem!', 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('register'))

        # Teste de depuração
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Anxiety: {anxiety}")
        print(f"Competitiveness: {competitiveness}")
        print(f"Genres: {', '.join(genres)}")
        print(f"Activities: {', '.join(activities)}")
        print(f"Motivations: {', '.join(motivations)}")

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
