"""Flask application factory + entry point.

Run with:  python app.py
Then open: http://localhost:5000
"""
import os

from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user

from config import Config
from models import User, db


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to enter the metaverse."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, "models_pkl"), exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from auth import auth_bp
    from metaverse import metaverse_bp
    from admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(metaverse_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            if current_user.is_admin:
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("metaverse.room"))
        return redirect(url_for("auth.login"))

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=True)
