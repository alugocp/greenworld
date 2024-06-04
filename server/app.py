"""
Entry point module for the Greenworld server
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
from flask import Flask
import sqlalchemy
import pages
import api
import lib
from greenworld import orm
from greenworld import Greenworld

app = Flask(
    "Greenworld",
    template_folder="server/templates",
    static_folder="server/static"
)


# Custom filters
@app.template_filter()
def citation_regex(href):
    """
    Provides the citation_regex function as a Flask/Jinja filter
    """
    return lib.citation_regex(href)


# Initialization method
def main():
    """
    Main method, entry for the Greenworld server
    """
    Greenworld()
    db = orm.init_db()

    # Import other server code
    pages.main(app, db)
    api.main(app, db)

    # Setup auth/login stuff
    app.config["SECRET_KEY"] = "secret-key-goes-here"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///server.db"
    flask_sql = SQLAlchemy()
    flask_sql.init_app(app)
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    # flask_sql.create_all(app=app)

    class User(UserMixin, flask_sql.Model):
        id = flask_sql.Column(flask_sql.Integer, primary_key=True)
        email = flask_sql.Column(flask_sql.String(100), unique=True)
        password = flask_sql.Column(flask_sql.String(100))
        name = flask_sql.Column(flask_sql.String(1000))

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # Run the server
    # TODO this function is not intended for production use, please rewrite before launch
    # https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.run
    app.run(host="0.0.0.0", port=2017)


# Main script
if __name__ == "__main__":
    main()
