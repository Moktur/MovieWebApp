from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

class User(db.Model):
    """
    Represents a user in the MoviWeb application.

    Each user can have multiple favorite movies associated with them.

    Attributes:
        id (int): Unique identifier for the user
        name (str): User's display name
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class Movie(db.Model):
    """
    Represents a movie in a user's favorite movies list.

    Each movie belongs to exactly one user and contains information
    fetched from OMDb API.

    Attributes:
        id (int): Unique identifier for the movie entry
        name (str): Title of the movie
        director (str): Director of the movie
        year (int): Year the movie was released
        poster_url (str): URL to the movie poster image
        user_id (int): Foreign key linking to the User who favorited this movie
    """
    __tablename__ = 'movies'
    # TODO evt unique=True bei name, director rausmachen
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    director = db.Column(db.String(100), unique=True, nullable=False)
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Movie {self.name} (ID: {self.id})>"

    def __str__(self):
        return f"{self.name}"
