from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    Represents a user in the MovieWeb application.

    Each user can have multiple favorite movies.

    Attributes:
        id (int): Unique identifier for the user.
        name (str): The display name of the user.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


class Movie(db.Model):
    """
    Represents a movie in a user's favorite movies list.

    Each movie belongs to exactly one user and contains information
    fetched from the OMDb API.

    Attributes:
        id (int): Unique identifier for the movie entry.
        name (str): Title of the movie.
        director (str): Director of the movie.
        year (int): Year the movie was released.
        poster_url (str): URL to the movie poster image.
        user_id (int): Foreign key linking to the User who favorited this movie.
    """
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        """Returns a debug representation of the Movie object."""
        return f"<Movie {self.name} (ID: {self.id})>"

    def __str__(self):
        """Returns a string representation of the Movie title."""
        return f"{self.name}"
