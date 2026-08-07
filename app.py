import os
from flask import Flask
from data_manager import DataManager
from models import db, Movie

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app

data_manager = DataManager()  # Create an object of your DataManager class


def initial_db():
    """Create the database tables. Execute only once at the first launch."""
    with app.app_context():
        db.create_all()


@app.route('/')
def home():
    """Home page route."""
    return "Welcome to MoviWeb App!"


@app.route('/users')
def list_users():
    """List all users."""
    users = data_manager.get_users()
    return str(users)  # Temporarily returning users as a string


if __name__ == '__main__':
    app.run(debug=True)
