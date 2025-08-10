from flask import Flask
from data_manager import DataManager
from models import db, Movie, User
from sqlalchemy import create_engine

app = Flask(__name__)

DB_URL = "sqlite:////home/pepe/PycharmMiscProjects/movieprojectflasksqlalchemy/data/moviewebapp.sqlite"
engine = create_engine(DB_URL, echo=False)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# linking database and app, reason why we need import models from db
db.init_app(app)
with app.app_context():
    db.create_all()
data_manager = DataManager(DB_URL)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)