from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    preferencias = db.Column(db.Text)
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_prefs(self, prefs_dict):
        """Set preferences as a JSON string."""
        self.preferencias = json.dumps(prefs_dict)

    def get_prefs(self):
        """Get preferences as a dictionary."""
        # Return an empty dictionary if preferencias is None
        if self.preferencias:
            return json.loads(self.preferencias)
        return {}

    def add_xp(self, amount):
        self.xp += amount
        if self.xp >= 100:
            self.level += 1  # Level up
            self.xp -= 100  # Reset XP after level up

    def get_latest_stress_record(self):
        """Get the latest stress record for the user."""
        return StressRecord.query.filter_by(user_id=self.id).order_by(StressRecord.date.desc()).first()

    def __repr__(self):
        return f'<User {self.name}>'


class StressRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stress_level = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('stress_records', lazy=True))

    def __repr__(self):
        return f'<StressRecord {self.stress_level} for User {self.user_id} on {self.date}>'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    game = db.relationship('Game', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f'<Comment {self.text} by User {self.user_id} on Game {self.game_id}>'


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(256))
    categorias = db.Column(db.Text)

    def set_categories(self, categories_list: list):
        self.categorias = json.dumps(categories_list)

    def get_categories(self):
        return json.loads(self.categorias)

    def average_rating(self):
        if not self.comments:
            return 0  # Return 0 if there are no ratings
        return sum(comment.rating for comment in self.comments) / len(self.comments)


    def __repr__(self):
        return f'<User {self.name}>'
