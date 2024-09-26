import os
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from app.models import db
from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.routes.game_routes import game_bp

load_dotenv()

app = Flask(__name__)

# config database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# can add prefix to the routes here if needed
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(game_bp)


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db.init_app(app)

migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')
