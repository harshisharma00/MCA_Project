"""Admin blueprint — dashboard, threats list, user management."""
from datetime import datetime, timedelta
from functools import wraps

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from models import Message, Threat, UrlShared, User, db


admin_bp = Blueprint("admin", __name__)


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return wrapper


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    stats = {
        "total_users": User.query.filter_by(role="user").count(),
        "banned_users": User.query.filter_by(is_banned=True).count(),
        "messages_today": Message.query.filter(Message.timestamp >= today_start).count(),
        "threats_today": Threat.query.filter(Threat.timestamp >= today_start).count(),
        "total_threats": Threat.query.count(),
        "toxic_total": Threat.query.filter_by(threat_type="toxicity").count(),
        "phishing_total": Threat.query.filter_by(threat_type="phishing").count(),
    }

    recent = (
        Threat.query.order_by(Threat.timestamp.desc())
        .limit(10)
        .all()
    )
    user_cache = {u.id: u for u in User.query.all()}

    return render_template(
        "admin_dashboard.html",
        stats=stats,
        recent=[
            {
                "id": t.id,
                "username": user_cache[t.user_id].username if t.user_id in user_cache else "?",
                "type": t.threat_type,
                "score": t.score,
                "payload": t.payload,
                "when": t.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for t in recent
        ],
    )


@admin_bp.route("/threats")
@login_required
@admin_required
def threats_view():
    type_filter = request.args.get("type", "")
    query = Threat.query
    if type_filter in ("toxicity", "phishing"):
        query = query.filter_by(threat_type=type_filter)

    rows = query.order_by(Threat.timestamp.desc()).limit(200).all()
    user_cache = {u.id: u for u in User.query.all()}

    return render_template(
        "admin_threats.html",
        type_filter=type_filter,
        threats=[
            {
                "id": t.id,
                "username": user_cache[t.user_id].username if t.user_id in user_cache else "?",
                "type": t.threat_type,
                "score": t.score,
                "payload": t.payload,
                "when": t.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for t in rows
        ],
    )


@admin_bp.route("/users")
@login_required
@admin_required
def users_view():
    rows = User.query.order_by(User.created_at.desc()).all()

    threat_counts = dict(
        db.session.query(Threat.user_id, func.count(Threat.id))
        .group_by(Threat.user_id)
        .all()
    )

    return render_template(
        "admin_users.html",
        users=[
            {
                "id": u.id,
                "username": u.username,
                "role": u.role,
                "color": u.avatar_color,
                "is_banned": u.is_banned,
                "threats": threat_counts.get(u.id, 0),
                "joined": u.created_at.strftime("%Y-%m-%d %H:%M"),
            }
            for u in rows
        ],
    )


@admin_bp.route("/users/<int:user_id>/ban", methods=["POST"])
@login_required
@admin_required
def ban_user(user_id: int):
    user = db.session.get(User, user_id)
    if user is None:
        abort(404)
    if user.is_admin:
        flash("Cannot ban an administrator.", "danger")
        return redirect(url_for("admin.users_view"))
    user.is_banned = True
    db.session.commit()
    flash(f"User '{user.username}' has been banned.", "warning")
    return redirect(url_for("admin.users_view"))


@admin_bp.route("/users/<int:user_id>/unban", methods=["POST"])
@login_required
@admin_required
def unban_user(user_id: int):
    user = db.session.get(User, user_id)
    if user is None:
        abort(404)
    user.is_banned = False
    db.session.commit()
    flash(f"User '{user.username}' has been unbanned.", "success")
    return redirect(url_for("admin.users_view"))


@admin_bp.route("/api/stats")
@login_required
@admin_required
def api_stats():
    """Live data feed for the dashboard — cards, charts, recent threats.

    Polled every few seconds by static/js/admin.js so the dashboard
    auto-updates without a page refresh.
    """
    now = datetime.utcnow()
    start = now - timedelta(hours=23)
    start = start.replace(minute=0, second=0, microsecond=0)

    rows = (
        db.session.query(Threat.timestamp, Threat.threat_type)
        .filter(Threat.timestamp >= start)
        .all()
    )

    buckets_tox = [0] * 24
    buckets_phi = [0] * 24
    labels = []
    for i in range(24):
        label_time = start + timedelta(hours=i)
        labels.append(label_time.strftime("%H:00"))

    for ts, ttype in rows:
        idx = int((ts - start).total_seconds() // 3600)
        if 0 <= idx < 24:
            if ttype == "toxicity":
                buckets_tox[idx] += 1
            elif ttype == "phishing":
                buckets_phi[idx] += 1

    type_counts = {
        "toxicity": Threat.query.filter_by(threat_type="toxicity").count(),
        "phishing": Threat.query.filter_by(threat_type="phishing").count(),
    }
    url_counts = {
        "phishing_urls": UrlShared.query.filter_by(is_phishing=True).count(),
        "clean_urls": UrlShared.query.filter_by(is_phishing=False).count(),
    }

    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    cards = {
        "total_users": User.query.filter_by(role="user").count(),
        "banned_users": User.query.filter_by(is_banned=True).count(),
        "messages_today": Message.query.filter(Message.timestamp >= today_start).count(),
        "threats_today": Threat.query.filter(Threat.timestamp >= today_start).count(),
    }

    recent_rows = Threat.query.order_by(Threat.timestamp.desc()).limit(10).all()
    user_cache = {u.id: u for u in User.query.all()}
    recent = [
        {
            "id": t.id,
            "username": user_cache[t.user_id].username if t.user_id in user_cache else "?",
            "type": t.threat_type,
            "score": t.score,
            "payload": t.payload,
            "when": t.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for t in recent_rows
    ]

    return jsonify({
        "labels": labels,
        "toxicity": buckets_tox,
        "phishing": buckets_phi,
        "type_counts": type_counts,
        "url_counts": url_counts,
        "cards": cards,
        "recent": recent,
        "server_time": now.strftime("%H:%M:%S"),
    })
