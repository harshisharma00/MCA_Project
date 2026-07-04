"""Authentication blueprint — register, login, logout."""
import random

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from models import User, db


auth_bp = Blueprint("auth", __name__)


AVATAR_PALETTE = [
    "#5DADE2", "#48C9B0", "#F4D03F", "#EB984E",
    "#AF7AC5", "#EC7063", "#52BE80", "#5499C7",
]


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not username or not password:
            flash("Username and password are required.", "danger")
            return render_template("register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("register.html")

        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "danger")
            return render_template("register.html")

        user = User(
            username=username,
            avatar_color=random.choice(AVATAR_PALETTE),
            x=random.randint(80, 700),
            y=random.randint(80, 420),
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash("Invalid username or password.", "danger")
            return render_template("login.html")

        if user.is_banned:
            flash("This account has been banned by an administrator.", "danger")
            return render_template("login.html")

        login_user(user)
        flash(f"Welcome, {user.username}!", "success")
        if user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("metaverse.room"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have left the metaverse.", "info")
    return redirect(url_for("auth.login"))
