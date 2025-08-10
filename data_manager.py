from sqlalchemy import create_engine, text
from models import db, User, Movie


class DataManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)


    def create_user(self, name):
        with self.engine.connect() as connection:
            try:
                connection.execute(text(
                    "INSERT INTO users(name) "
                    "VALUES (:name)"),
                    {"name":name}
                )
                connection.commit()
                print(f"User {name} added successfully.")
            except Exception as e:
                print(f"Something went wrong: {e}")


    def get_users(self):
        with self.engine.connect() as connection:
            result = connection.execute(text(
                "SELECT name FROM users")
                )
            users = result.fetchall()
            return [row[0] for row in users]


    def get_movies(self, user_id):
        """Retrieve all movies from the database from a specific user."""
        with self.engine.connect() as connection:
            query = text("""
                SELECT name, director, year, poster_url FROM movies
                WHERE user_id= :user_id
                """)
            result = connection.execute(query, {"user_id": user_id})
            movies = result.fetchall()
            return [
                    {
                    'name': row[0],
                    'director': row[1],
                    'year': row[2],
                    'poster_url': row[3]
                    } for row in movies
                ]


    def add_movie(self, movie): # NOTE movie ist ein Objekt
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
        try:
            with self.engine.connect() as connection:
                moviename = ""
                query_for_select = text("""
                    SELECT name FROM movies
                    WHERE id = :movie_id
                    """)
                query_for_select_keys = {"movie_id":movie_id}
                result_select = connection.execute(query_for_select, query_for_select_keys)
                row = result_select.fetchone()
                try:
                    moviename = row[0]
                except TypeError:
                    raise ValueError(f"Movie with ID {movie_id} not found")
                query = text("""
                    UPDATE movies
                    SET name = :new_title
                    WHERE id = :movie_id
                    """)
                query_keys = {"new_title": new_title, "movie_id": movie_id}

                result = connection.execute(query, query_keys)
                if result.rowcount == 1:
                    print(f"Movie {moviename} successfully updated to {new_title}")
                    connection.commit()

        except Exception as e:
            print(f"Something went wrong!: {e}")


    def delete_movie(self, movie):
        with self.engine.connect() as connection:
            try:
                query = text("""
                    DELETE FROM movies
                    WHERE id = :id
                    """)
                query_key = {"id":movie.id}
                result = connection.execute(query, query_key).rowcount
                if result == 1:
                    connection.commit()
                if result <= 0:
                    raise ValueError(f"Movie {movie.name} not found in database.")
            except Exception as e:
                print(f"Something went wrong: {e}")