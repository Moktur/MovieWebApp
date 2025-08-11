from sqlalchemy import create_engine, text
from flask import abort
from models import db, User, Movie


class DataManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)


    def create_user(self, name):
        with self.engine.connect() as connection:
            try:
                if not self.find_user(name):

                    connection.execute(text(
                        "INSERT INTO users(name) "
                        "VALUES (:name)"),
                        {"name":name}
                    )
                    connection.commit()
                    print(f"User {name} added successfully.")
                else:
                    raise ValueError(f"{name} already in Database. Please choose a different name.")
            except Exception as e:
                print(f"Something went wrong: {e}")


    def get_users(self):
        with self.engine.connect() as connection:
            result = connection.execute(text(
                "SELECT id, name FROM users")
                )
            users = result.fetchall()
            # This List will contain the objects of User
            user_object_list = []

            for row in users:
                user = User()
                user.id = row[0]
                user.name = row[1]
                user_object_list.append(user)
            return user_object_list


    def get_user(self,id):
        with self.engine.connect() as connection:
            query = text("""
                    SELECT id, name FROM users
                    WHERE id = :id
                    """)
            query_key = {"id":id}
            result = connection.execute(query, query_key)
            row = result.fetchone()
            if row:
                user = User()
                user.id, user.name = row[0], row[1]
                return user
            else:
                abort(404, description=f"User with ID {id} not found.")


    def find_user(self, name):
        with self.engine.connect() as connection:
            query = text("""
            SELECT name FROM users
            WHERE name = :name
            """)
            query_key = {"name": name}
            result = connection.execute(query,query_key)
            # Check if user already exist in database
            row = result.fetchone()
            if row:
                return True
            return False



    def get_movies(self, user_id):
        """Retrieve all movies from the database from a specific user."""
        with self.engine.connect() as connection:
            query = text("""
                SELECT id, name, director, year, poster_url FROM movies
                WHERE user_id= :user_id
                """)
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


    def delete_movie(self, movie_id):
        with self.engine.connect() as connection:
            try:
                query = text("""
                    DELETE FROM movies
                    WHERE id = :id
                    """)
                query_key = {"id":movie_id}
                result = connection.execute(query, query_key).rowcount
                if result == 1:
                    connection.commit()
                    return True
                if result <= 0:
                    raise ValueError(f"Movie {movie_id} not found in database.")
            except Exception as e:
                print(f"Something went wrong: {e}")



    def generate_fake_users(self):
        """Add test users via SQLAlchemy session with Vietnamese historical figures"""
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