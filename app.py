import os
from flask import Flask, render_template, request, flash, redirect, url_for
from data_manager import DataManager
from models import db, Movie

app = Flask(__name__)
# TODO! app config secret_key

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
    """Home page route. List the users and a form to create a new one."""
    users = data_manager.get_users()
    return render_template("home.html", users=users)

# TODO! home.html pendiente


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

    # OMDb API call

    # new_movie = Movie(name=title, ...)

    # data_manager.add_movie(movie)

    # flash(f"Movie '{title}' added successfully.", "success")

    # return redirect(url_for("user_movies", user_id=user_id))


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
