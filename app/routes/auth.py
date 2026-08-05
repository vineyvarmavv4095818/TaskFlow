from flask import Blueprint, render_template, request, url_for, flash, session, redirect
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)



@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists!", "danger")
            return redirect(url_for("auth.register"))

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create new user
        new_user = User(
            username=username,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Find user in database
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            # Store logged-in user in session
            session["user"] = user.username

            flash("Login Successful!", "success")

            return redirect(url_for("tasks.view_tasks"))

        else:
            flash("Invalid username or password!", "danger")

    return render_template("login.html")



@auth_bp.route("/logout")
def logout():
    session.pop('user', None)
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))