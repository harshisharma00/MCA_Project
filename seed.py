"""Seed the database with one admin and two demo users.

Run from project root:
    python seed.py

Idempotent — safe to run multiple times.
"""
from app import create_app
from models import User, db


DEMO_USERS = [
    # username, password, role, color, x, y
    ("admin", "admin123", "admin", "#F4D03F", 100, 100),
    ("alice", "password123", "user", "#5DADE2", 200, 200),
    ("bob",   "password123", "user", "#48C9B0", 500, 300),
]


def main() -> None:
    app = create_app()
    with app.app_context():
        db.create_all()
        for username, password, role, color, x, y in DEMO_USERS:
            existing = User.query.filter_by(username=username).first()
            if existing:
                print(f"[seed] '{username}' already exists, skipping.")
                continue
            user = User(
                username=username,
                role=role,
                avatar_color=color,
                x=x,
                y=y,
            )
            user.set_password(password)
            db.session.add(user)
            print(f"[seed] Created {role} '{username}'.")
        db.session.commit()
        print("[seed] Done.")


if __name__ == "__main__":
    main()
