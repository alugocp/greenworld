"""
This module handles user login to the Greenworld server
"""

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_required
from flask_login import logout_user
from flask_login import login_user
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

# Top-level objects for export
auth = Blueprint("auth", __name__)
flask_sql = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def main(app):
    """
    Initialize user database with the Flask App instance
    """
    app.config["SECRET_KEY"] = "secret-key-goes-here"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///server.db"
    flask_sql.init_app(app)
    app.register_blueprint(auth)
    login_manager.init_app(app)
    with app.app_context():
        flask_sql.create_all()

    # Add the data submission endpoint
    @app.route("/submission")
    @login_required
    def submission_endpoint():
        return render_template("submission.html")


# Model for the User table
class User(UserMixin, flask_sql.Model):
    """
    Represents the user data stored in the database
    """

    id = flask_sql.Column(flask_sql.Integer, primary_key=True)
    email = flask_sql.Column(flask_sql.String(100), unique=True)
    password = flask_sql.Column(flask_sql.String(100))
    accepted = flask_sql.Column(flask_sql.Boolean, default = False)


# TODO use this somewhere
@login_manager.user_loader
def load_user(user_id):
    """
    Retrieves an entry from the User model
    """
    return User.query.get(int(user_id))


#
# ROUTE ENDPOINTS
#


@auth.route("/login")
def login():
    """
    Renders the login page
    """
    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    """
    Renders the logout page
    """
    logout_user()
    return redirect("/")


#
# FORM HANDLER ENDPOINTS
#


@auth.route("/login", methods=["POST"])
def login_post():
    """
    Validates and logs in a new user
    """
    email = request.form.get("email")
    password = request.form.get("password")
    remember = bool(request.form.get("remember"))

    # Log user in if their password is correct
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Password is incorrect or user does not exist.")
        return redirect(url_for("auth.login"))
    login_user(user, remember=remember)
    return redirect("/submission")


@auth.route("/signup", methods=["POST"])
def signup_post():
    """
    Validates and registers a new user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    # Make sure user doesn't already exist
    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email address is already in use with this server")
        return redirect(url_for("auth.signup"))

    # Register the new user and go to login
    new_user = User(email = email, password = generate_password_hash(password))
    flask_sql.session.add(new_user)
    flask_sql.session.commit()
    login_user(new_user)
    return redirect("/submission")
