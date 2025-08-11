from sqlalchemy import create_engine, text
from flask import abort
from models import db, User, Movie


class DataManager:
    """Handles database operations for users and movies."""

    def __init__(self, db_url):
        """Initialize the DataManager with a database connection.

        Args:
            db_url (str): SQLAlchemy database URL.
        """
        self.engine = create_engine(db_url)


    def create_user(self, name):
        """Create a new user in the database.

        Args:
            name (str): Name of the user.

        Raises:
            ValueError: If the user already exists.
        """
        with self.engine.connect() as connection:
            try:
                if not self.find_user(name):
                    connection.execute(
                        text("INSERT INTO users(name) VALUES (:name)"),
                        {"name": name}
                    )
                    connection.commit()
                    print(f"User {name} added successfully.")
                else:
                    raise ValueError(f"{name} already in Database. Please choose a different name.")
            except Exception as e:
                print(f"Something went wrong: {e}")


    def get_users(self):
        """Retrieve all users from the database.

        Returns:
            list: List of User objects.
        """
        with self.engine.connect() as connection:
            result = connection.execute(text("SELECT id, name FROM users"))
            users = result.fetchall()
            user_object_list = []

            for row in users:
                user = User()
                user.id = row[0]
                user.name = row[1]
                user_object_list.append(user)
            return user_object_list


    def get_user(self, id):
        """Retrieve a user by ID.

        Args:
            id (int): User ID.

        Returns:
            User: User object.

        Raises:
            werkzeug.exceptions.NotFound: If the user is not found.
        """
        with self.engine.connect() as connection:
            query = text("SELECT id, name FROM users WHERE id = :id")
            result = connection.execute(query, {"id": id})
            row = result.fetchone()
            if row:
                user = User()
                user.id, user.name = row[0], row[1]
                return user
            else:
                abort(404, description=f"User with ID {id} not found.")


    def find_user(self, name):
        """Check if a user exists in the database.

        Args:
            name (str): Name of the user.

        Returns:
            bool: True if the user exists, otherwise False.
        """
        with self.engine.connect() as connection:
            query = text("SELECT name FROM users WHERE name = :name")
            result = connection.execute(query, {"name": name})
            return result.fetchone() is not None


    def get_movies(self, user_id):
        """Retrieve all movies for a specific user.

        Args:
            user_id (int): User ID.

        Returns:
            list: List of Movie objects.
        """
        with self.engine.connect() as connection:
            query = text(
                "SELECT id, name, director, year, poster_url FROM movies WHERE user_id= :user_id"
            )
            result = connection.execute(query, {"user_id": user_id})
            movies = []
            for row in result.fetchall():
                movie = Movie()
                movie.id = row[0]
                movie.name = row[1]
                movie.director = row[2]
                movie.year = row[3]
                movie.poster_url = row[4]
                movies.append(movie)
            return movies


    def add_movie(self, movie):
        """Add a new movie to the database.

        Args:
            movie (Movie): Movie object to add.
        """
        with self.engine.connect() as connection:
            query = text("""
                INSERT INTO movies(name, director, year, poster_url, user_id)
                VALUES (:name, :director, :year, :poster_url, :user_id)
            """)
            query_keys = {
                "name": movie.name,
                "director": movie.director,
                "year": movie.year,
                "poster_url": movie.poster_url,
                "user_id": movie.user_id
            }
            try:
                connection.execute(query, query_keys)
                connection.commit()
                print(f"Movie {movie} added successfully.")
            except Exception as e:
                print(f"Something went wrong: {e}")


    def update_movie(self, movie_id, new_title):
        """Update the title of a movie.

        Args:
            movie_id (int): ID of the movie to update.
            new_title (str): New movie title.

        Raises:
            ValueError: If the movie is not found.
        """
        try:
            with self.engine.connect() as connection:
                query_for_select = text("SELECT name FROM movies WHERE id = :movie_id")
                row = connection.execute(query_for_select, {"movie_id": movie_id}).fetchone()
                if not row:
                    raise ValueError(f"Movie with ID {movie_id} not found")
                moviename = row[0]

                query = text("UPDATE movies SET name = :new_title WHERE id = :movie_id")
                result = connection.execute(query, {"new_title": new_title, "movie_id": movie_id})
                if result.rowcount == 1:
                    print(f"Movie {moviename} successfully updated to {new_title}")
                    connection.commit()
        except Exception as e:
            print(f"Something went wrong!: {e}")


    def delete_movie(self, movie_id):
        """Delete a movie from the database.

        Args:
            movie_id (int): ID of the movie to delete.

        Returns:
            bool: True if the movie was deleted.

        Raises:
            ValueError: If the movie does not exist.
        """
        with self.engine.connect() as connection:
            try:
                query = text("DELETE FROM movies WHERE id = :id")
                result = connection.execute(query, {"id": movie_id}).rowcount
                if result == 1:
                    connection.commit()
                    return True
                else:
                    raise ValueError(f"Movie {movie_id} not found in database.")
            except Exception as e:
                print(f"Something went wrong: {e}")


    def generate_fake_users(self):
        """Insert predefined test users into the database."""
        stmt = text("""
            INSERT INTO users (name) VALUES
            ('Nguyễn Trãi'),
            ('Trần Hưng Đạo'),
            ('Lê Lợi'),
            ('Nguyễn Thị Minh Khai'),
            ('Phan Bội Châu'),
            ('Nguyễn Huệ'),
            ('Võ Nguyên Giáp')
        """)
        db.session.execute(stmt)
        db.session.commit()
        print("⛏✡ Test-Users added! ✡⛏")
