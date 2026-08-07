import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for
from data_manager import DataManager
from models import db, Movie

load_dotenv()
API_KEY = os.environ.get('OMDB_API_KEY')
OMDB_URL = "http://www.omdbapi.com/"

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db.init_app(app)

data_manager = DataManager()


def initial_db():
    """Create the database tables. Execute only once at the first launch."""
    with app.app_context():
        db.create_all()


def fetch_movie_from_omdb(title):
    """Fetch information about a movie from OMDb API."""
    if not API_KEY:
        print("Warning: OMDb API key not set.")
        return None
    url = f"{OMDB_URL}?apikey={API_KEY}&t={title}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching movie from OMDb API: {e}")
        return None

    year_raw = data.get("Year", "")
    year_digits = "".join(ch for ch in year_raw if ch.isdigit())[:4]
    movie_data = {
        "name": data.get("Title", title),
        "director": data.get("Director"),
        "year": int(year_digits) if year_digits else None,
        "poster_url": data.get("Poster")
    }
    return movie_data


@app.route('/')
def home():
    """Home page route. List the users and a form to create a new one."""
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """Process the form submission to create a new user."""
    name = request.form.get("name", "").strip()
    if not name:
        flash("Name is required.", "error")
        return redirect(url_for("home"))
    data_manager.create_user(name)
    flash(f"User '{name}' created successfully.", "success")
    return redirect(url_for("home"))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):
    """Display the list of movies for a specific user."""
    user = data_manager.get_user(user_id)
    if user is None:
        flash("User not found.", "error")
        return redirect(url_for("home"))

    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", user=user, movies=movies)

# TODO! movies.html pendiente


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Add a new movie to a user's list, it fetches movie's info from OMDb API."""
    user = data_manager.get_user(user_id)
    if user is None:
        flash("User not found.", "error")
        return redirect(url_for("home"))

    title = request.form.get("title", "").strip()
    if not title:
        flash("Title is required.", "error")
        return redirect(url_for("user_movies", user_id=user_id))

    omdb_info = fetch_movie_from_omdb(title)
    if omdb_info:
        new_movie = Movie(
            name=omdb_info["name"],
            director=omdb_info["director"],
            year=omdb_info["year"],
            poster_url=omdb_info["poster_url"],
            user_id=user_id
        )
        data_manager.add_movie(new_movie)
        flash(f"Movie '{omdb_info['name']}' added successfully.", "success")
    else:
        new_movie = Movie(
            name=title,
            user_id=user_id
        )
        data_manager.add_movie(new_movie)
        flash(f'"{title}" added, but no info from OMDb API', "warning")
    return redirect(url_for("user_movies", user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Update a movie's title."""
    user = data_manager.get_user(user_id)
    if user is None:
        flash("User not found.", "error")
        return redirect(url_for("home"))

    new_title = request.form.get("title", "").strip()
    if not new_title:
        flash("Title is required.", "error")
        return redirect(url_for("user_movies", user_id=user_id))

    movie = data_manager.update_movie(movie_id, new_title)
    if movie is None:
        flash("Movie not found.", "error")
    else:
        flash(f"Movie '{movie.name}' updated successfully.", "success")
    return redirect(url_for("user_movies", user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Deletes a movie from the user's list."""
    user = data_manager.get_user(user_id)
    if user is None:
        flash("User not found.", "error")
        return redirect(url_for("home"))

    if data_manager.delete_movie(movie_id):
        flash(f"Movie '{movie_id}' deleted successfully.", "success")
    else:
        flash("Movie not found.", "error")
    return redirect(url_for("user_movies", user_id=user_id))


if __name__ == '__main__':
    app.run(debug=True)
