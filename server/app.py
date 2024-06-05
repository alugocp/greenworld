"""
Entry point module for the Greenworld server
"""

from flask import Flask
import sqlalchemy
import pages
import api
import lib
from greenworld import orm
from greenworld import Greenworld
from auth import flask_sql
from auth import login_manager
from auth import auth as auth_blueprint

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
    flask_sql.init_app(app)
    app.register_blueprint(auth_blueprint)
    login_manager.init_app(app)
    with app.app_context():
        flask_sql.create_all()

    # Run the server
    # TODO this function is not intended for production use, please rewrite before launch
    # https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.run
    app.run(host="0.0.0.0", port=2017)


# Main script
if __name__ == "__main__":
    main()
