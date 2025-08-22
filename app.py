from flask import Flask, render_template, request, redirect, url_for, flash, abort
from sqlalchemy import create_engine
from pathlib import Path
from data_manager import DataManager
from models import db, Movie
from movie_data_fetcher import fetch_data

app = Flask(__name__)
BASE_DIR = Path(__file__).parent.resolve()
db_path = BASE_DIR.joinpath("data", "moviewebapp.sqlite")

DB_URL = f"sqlite:///{db_path}"
engine = create_engine(DB_URL, echo=False)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SECRET_KEY'] = 'eine_sehr_lange_zufaellige_zeichenkette'

data_manager = DataManager(DB_URL)

# Link database and app
db.init_app(app)
with app.app_context():
    db.create_all()
    # data_manager.generate_fake_users()


@app.route('/')
def index():
    """Render the index page with a list of users."""
    users = data_manager.get_users()
    print(f"Users found: {users}")
    return render_template("index.html", users=users)


@app.route('/add_user', methods=['POST'])
def create_user():
    """Create a new user from form data and redirect to index."""
    if request.method == 'POST':
        name = request.form['user_name']
        if not data_manager.find_user(name):
            data_manager.create_user(name)
            return redirect(url_for('index'))
        flash(f"User '{name}' already in Database!", "error")
        return redirect(url_for('index'))



@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    """Display movies for a specific user.

    Args:
        user_id (int): The ID of the user.

    Raises:
        404: If the user is not found.
    """
    user = data_manager.get_user(user_id)
    if user:
        usermovielist = data_manager.get_movies(user_id)
        return render_template(
            "movies.html",
            usermovielist=usermovielist,
            user=user
        )
    abort(404, description="User not found")


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Add a movie to a user's collection.

    Args:
        user_id (int): The ID of the user.
    """
    if request.method == 'POST':
        name = request.form["title"]
        usermovielist = data_manager.get_movies(user_id)
        for movie in usermovielist:
            if name == movie.name:
                flash(f"Movie '{movie.name}' already in Database!", "error")
                return redirect(url_for('get_movies', user_id=user_id))
        moviedata = fetch_data(name)
        if moviedata:
            movie = Movie()
            movie.name = moviedata["Title"]
            movie.year = moviedata["Year"]
            movie.director = moviedata["Director"]
            movie.poster_url = moviedata["Poster"]
            movie.user_id = user_id
            data_manager.add_movie(movie)
            flash(f"Movie '{movie.name}' added successfully!", "success")
            return redirect(url_for('get_movies', user_id=user_id))
        else:
            flash(f"Can't find Movie", "error")
            return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Update a movie's details for a user.

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie.
    """
    if request.method == 'POST':
        name = request.form.get("title")
        if name:
            data_manager.update_movie(movie_id, name)
            return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Delete a movie from a user's collection.

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie.
    """
    if request.method == 'POST':
        if data_manager.delete_movie(movie_id):
            return redirect(url_for('get_movies', user_id=user_id))

    flash("Due Deleting, something went wrong")
    return redirect(url_for('get_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(error):
    """Render custom 404 error page."""
    return render_template(
        "error.html",
        error_code=404,
        error_name="Page Not Found",
        error_description=error.description if \
        hasattr(error, "description") else \
        "The page you requested does not exist."
    ), 404


@app.errorhandler(403)
def forbidden(error):
    """Render custom 403 forbidden page."""
    return render_template(
        "error.html",
        error_code=403,
        error_name="Forbidden",
        error_description=error.description if \
        hasattr(error, 'description') else \
        "You do not have permission to view this page."
    ), 403


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
