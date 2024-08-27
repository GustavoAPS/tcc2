from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    preferencias = db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_prefs(self, prefs_dict):
        self.preferencias = json.dumps(prefs_dict)

    def get_prefs(self):
        return self.preferencias

    def __repr__(self):
        return f'<User {self.name}>'


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(256))
    categorias = db.Column(db.Text)

    def set_categories(self, categories_list: list):
        self.categorias = json.dumps(categories_list)

    def get_categories(self):
        if self.categorias:
            return self.categorias
        return []

    def __repr__(self):
        return f'<User {self.name}>'
