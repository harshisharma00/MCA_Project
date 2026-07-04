"""SQLAlchemy ORM models for the Metaverse Threat Detection system."""
from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """A metaverse participant. role='admin' unlocks the dashboard."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default="user", nullable=False)
    avatar_color = db.Column(db.String(7), default="#5DADE2", nullable=False)
    x = db.Column(db.Integer, default=100, nullable=False)
    y = db.Column(db.Integer, default=100, nullable=False)
    is_banned = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    messages = db.relationship("Message", backref="user", lazy=True)
    threats = db.relationship("Threat", backref="user", lazy=True)

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"


class Message(db.Model):
    """Every chat message — including the ones we blocked.

    Blocked messages are kept (with is_threat=True) for the admin
    audit trail, but they are never broadcast to other users.
    """

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_threat = db.Column(db.Boolean, default=False, nullable=False)
    threat_score = db.Column(db.Float, default=0.0, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)


class Threat(db.Model):
    """One row per detected threat (toxicity or phishing)."""

    __tablename__ = "threats"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey("messages.id"), nullable=True)
    threat_type = db.Column(db.String(20), nullable=False)  # 'toxicity' | 'phishing'
    score = db.Column(db.Float, nullable=False)
    payload = db.Column(db.Text, nullable=False)  # the offending text or URL
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)


class UrlShared(db.Model):
    """Every URL that flowed through chat — useful for phishing analytics."""

    __tablename__ = "urls_shared"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    is_phishing = db.Column(db.Boolean, default=False, nullable=False)
    score = db.Column(db.Float, default=0.0, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
