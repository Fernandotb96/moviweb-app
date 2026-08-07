from models import db, User, Movie


class DataManager:
    """Manage the CRUD operations for users and movies."""

    # Users

    def create_user(self, name):
        """
        Create a new user and save it to the database.
        Returns the newly created User object (already with its id assigned).
        """
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_users(self):
        """Return a list of all users."""
        return User.query.all()

    def get_user(self, user_id):
        """Return a single user by id, or None if it doesn't exist."""
        return db.session.get(User, user_id)

    # Movies

    def get_movies(self, user_id):
        """Return the list of favorite movies for a specific user."""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """Add a new movie to a user's list of favorites."""
        db.session.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, movie_id, new_title):
        """
        Update the name/title of an existing movie.
        Returns the updated movie, or None if it wasn't found.
        """
        movie = db.session.get(Movie, movie_id)
        if movie is None:
            return None
        movie.name = new_title
        db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        """
        Delete a movie from the database by its id.
        Returns True if it was deleted successfully, False if it wasn't found.
        """
        movie = db.session.get(Movie, movie_id)
        if movie is None:
            return False
        db.session.delete(movie)
        db.session.commit()
        return True
