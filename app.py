from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from data_manager import DataManager
from models import db, Movie, User
from sqlalchemy import create_engine
from movie_data_fetcher import fetch_data

app = Flask(__name__)

DB_URL = "sqlite:////home/pepe/PycharmMiscProjects/movieprojectflasksqlalchemy/data/moviewebapp.sqlite"
engine = create_engine(DB_URL, echo=False)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SECRET_KEY'] = 'eine_sehr_lange_zufaellige_zeichenkette'
# linking database and app, reason why we need import models from db
db.init_app(app)
with app.app_context():
    db.create_all()


data_manager = DataManager(DB_URL)


# data_manager.generate_fake_users()

@app.route('/')
def index():
    users = data_manager.get_users()
    print(f"Users found: {users}")
    return render_template("index.html", users=users)


@app.route('/add_user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['user_name']
        data_manager.create_user(name)
        return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods= ['GET'])
def get_movies(user_id):
    user = data_manager.get_user(user_id)
    if user:
        usermovielist = data_manager.get_movies(user_id)
        return render_template(
            "movies.html",
            usermovielist=usermovielist,
            user=user
            )
    # if user is None
    abort(404, description="User not found")


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    if request.method == 'POST':
        # check if movie already exist
        name = request.form["title"]
        usermovielist = data_manager.get_movies(user_id)
        for movie in usermovielist:
            if name == movie.name:
                flash("Movie already in Database", "error")
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
            return redirect(url_for('get_movies', user_id=user_id))
        else:
            flash(f"Error finding Movie!")
            return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        name = request.form.get("title")
        # implementatin for future
        # year = request.form["year"]
        if name:
            data_manager.update_movie(movie_id, name)
            return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    if request.method == 'POST':
        if data_manager.delete_movie(movie_id):
            return redirect(url_for('get_movies', user_id=user_id))
        else:
            flash("Due Deleting, something went wrong")
            return redirect(url_for('get_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "error.html",
        error_code=404,
        error_name="Page Not Found",
        error_description=error.description if \
        hasattr(error,"description") else \
        "The page you requested does not exist."), 404





@app.errorhandler(403)
def forbidden(error):
    return render_template(
        "error.html",
        error_code=403,
        error_name="Forbidden",
        error_description=error.description if\
        hasattr(error, 'description') else \
        "You do not have permission to view this page."), 403
# def get_information_for_all_movies(movielist):
#     movie_object_list = []
#     for movie in movielist:

#         movie = Movie()
#         data = fetch_data(movie)
#         movie.name = data["Title"]
#         movie.year = data["Year"]
#         movie.director = data["Director"]
#         movie.poster_url = data["Poster"]



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)