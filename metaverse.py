"""Metaverse blueprint — 2D room, chat, threat detection hooks."""
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from ai.phishing_detector import get_detector as get_phishing_detector
from ai.toxicity_detector import get_detector as get_toxicity_detector
from ai.url_features import find_urls_in_text
from config import Config
from models import Message, Threat, UrlShared, User, db


metaverse_bp = Blueprint("metaverse", __name__)


@metaverse_bp.route("/room")
@login_required
def room():
    if current_user.is_banned:
        return "Your account is banned.", 403
    return render_template(
        "metaverse.html",
        room_width=Config.ROOM_WIDTH,
        room_height=Config.ROOM_HEIGHT,
        avatar_radius=Config.AVATAR_RADIUS,
    )


@metaverse_bp.route("/api/positions")
@login_required
def positions():
    """Return every active user's avatar position."""
    users = User.query.filter_by(role="user", is_banned=False).all()
    return jsonify({
        "me": current_user.id,
        "users": [
            {
                "id": u.id,
                "username": u.username,
                "x": u.x,
                "y": u.y,
                "color": u.avatar_color,
            }
            for u in users
        ],
    })


@metaverse_bp.route("/api/move", methods=["POST"])
@login_required
def move():
    """Update the current user's avatar position."""
    if current_user.is_banned:
        return jsonify({"error": "banned"}), 403
    data = request.get_json(silent=True) or {}
    try:
        new_x = int(data.get("x", current_user.x))
        new_y = int(data.get("y", current_user.y))
    except (TypeError, ValueError):
        return jsonify({"error": "invalid coordinates"}), 400

    r = Config.AVATAR_RADIUS
    new_x = max(r, min(Config.ROOM_WIDTH - r, new_x))
    new_y = max(r, min(Config.ROOM_HEIGHT - r, new_y))

    current_user.x = new_x
    current_user.y = new_y
    db.session.commit()
    return jsonify({"x": new_x, "y": new_y})


@metaverse_bp.route("/api/messages")
@login_required
def get_messages():
    """Return last 50 non-threat messages from the past 30 minutes."""
    since = datetime.utcnow() - timedelta(minutes=30)
    rows = (
        Message.query
        .filter(Message.is_threat == False, Message.timestamp >= since)
        .order_by(Message.timestamp.asc())
        .limit(50)
        .all()
    )
    user_cache = {u.id: u for u in User.query.all()}
    return jsonify({
        "messages": [
            {
                "id": m.id,
                "user_id": m.user_id,
                "username": user_cache[m.user_id].username if m.user_id in user_cache else "?",
                "color": user_cache[m.user_id].avatar_color if m.user_id in user_cache else "#888",
                "content": m.content,
                "timestamp": m.timestamp.isoformat() + "Z",
            }
            for m in rows
        ]
    })


@metaverse_bp.route("/api/chat/send", methods=["POST"])
@login_required
def send_message():
    """The core threat-detection pipeline."""
    if current_user.is_banned:
        return jsonify({"blocked": True, "reason": "banned"}), 403

    data = request.get_json(silent=True) or {}
    text = (data.get("content") or "").strip()
    if not text:
        return jsonify({"blocked": True, "reason": "empty"}), 400
    if len(text) > 500:
        return jsonify({"blocked": True, "reason": "too long"}), 400

    # 1) Toxicity check on the whole message
    is_toxic, tox_score = get_toxicity_detector().predict(text)

    # 2) Phishing check on every URL in the message
    urls = find_urls_in_text(text)
    phishing_hits = []
    phishing_detector = get_phishing_detector()
    for url in urls:
        is_phish, ph_score = phishing_detector.predict(url)
        # Always record the URL for analytics
        db.session.add(UrlShared(
            user_id=current_user.id,
            url=url,
            is_phishing=is_phish,
            score=ph_score,
        ))
        if is_phish:
            phishing_hits.append((url, ph_score))

    is_threat = is_toxic or bool(phishing_hits)

    msg = Message(
        user_id=current_user.id,
        content=text,
        is_threat=is_threat,
        threat_score=max(tox_score,
                         max((s for _, s in phishing_hits), default=0.0)),
    )
    db.session.add(msg)
    db.session.flush()

    if is_toxic:
        db.session.add(Threat(
            user_id=current_user.id,
            message_id=msg.id,
            threat_type="toxicity",
            score=tox_score,
            payload=text,
        ))
    for url, ph_score in phishing_hits:
        db.session.add(Threat(
            user_id=current_user.id,
            message_id=msg.id,
            threat_type="phishing",
            score=ph_score,
            payload=url,
        ))

    db.session.commit()

    if is_threat:
        reasons = []
        if is_toxic:
            reasons.append(f"toxic content (score {tox_score:.2f})")
        if phishing_hits:
            top = phishing_hits[0]
            reasons.append(f"phishing URL {top[0]!r} (score {top[1]:.2f})")
        return jsonify({
            "blocked": True,
            "reason": " and ".join(reasons),
            "toxic": is_toxic,
            "toxic_score": tox_score,
            "phishing": bool(phishing_hits),
            "phishing_urls": [u for u, _ in phishing_hits],
        })

    return jsonify({"blocked": False, "id": msg.id})
