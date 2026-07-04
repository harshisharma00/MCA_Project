# MetaGuard — Metaverse Threat Detection AI

**MCA Final Year Project — Chandigarh University**

A working prototype that simulates a small metaverse and uses **AI / Machine
Learning** to detect two real-world online threats in real time:

1. **Toxic / abusive chat messages** — TF-IDF + Logistic Regression text classifier.
2. **Phishing / malicious URLs** shared inside the chat — hand-crafted URL
   features + Logistic Regression.

Detected threats are blocked from reaching other users, logged to a database,
and surfaced on a **moderator dashboard** with live charts. Moderators can
ban repeat offenders.

---

## Features

- Multi-user 2D **metaverse room** (HTML5 Canvas) — avatars walk around with
  arrow keys / WASD and chat in real time.
- Two trained scikit-learn ML models running on the Flask server.
- Every chat message goes through the AI before it is broadcast.
- **Admin dashboard** with Chart.js visualisations:
  - Threats per hour (last 24 hours)
  - Toxicity vs phishing split (doughnut)
  - Recent threats table + full searchable threats list
  - User management with ban / unban
- SQLite storage — zero setup.
- Pure Python + browser — no Docker, no cloud, no GPU, no internet at runtime.

---

## Architecture

```
Browser (User)                Browser (Admin)
   │                              │
   │ HTTP / fetch                 │
   ▼                              ▼
┌─────────────────────────────────────────────┐
│            Flask Web App (app.py)           │
│  ┌──────────┬──────────┬──────────────────┐ │
│  │  auth    │ metaverse│  admin           │ │
│  │ blueprint│ blueprint│  blueprint       │ │
│  └────┬─────┴────┬─────┴─────────┬────────┘ │
│       │          │               │          │
│       │   ┌──────▼─────────┐     │          │
│       │   │ AI detectors   │     │          │
│       │   │ toxicity + URL │     │          │
│       │   └──────┬─────────┘     │          │
│       │          │               │          │
│       ▼          ▼               ▼          │
│   SQLAlchemy ORM ────► SQLite (metaverse.db)│
└─────────────────────────────────────────────┘
```

A more detailed walkthrough is in [`docs/architecture.md`](docs/architecture.md).

---

## Folder layout

```
MCA_Project/
├── app.py                # Flask app factory + entry point
├── config.py             # Secret key, DB URI, model paths, thresholds
├── models.py             # SQLAlchemy models
├── auth.py               # /register, /login, /logout
├── metaverse.py          # /room, /api/chat/send, /api/positions, /api/move
├── admin.py              # /admin, /admin/threats, /admin/users
├── seed.py               # Creates admin + alice + bob
│
├── ai/
│   ├── toxicity_detector.py
│   ├── phishing_detector.py
│   ├── url_features.py
│   ├── train_toxicity.py
│   └── train_phishing.py
│
├── data/
│   ├── toxic_comments.csv   # ~390 labelled chat messages
│   └── phishing_urls.csv    # ~390 labelled URLs
│
├── models_pkl/            # Trained models (created by training scripts)
├── static/                # CSS + JS
├── templates/             # Jinja2 templates
├── instance/              # SQLite DB lives here
│
├── requirements.txt
├── README.md              ← you are here
└── docs/
    ├── architecture.md
    └── project_report_outline.md
```

---

## Getting started

### 1. Install Python 3.10+ and create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the AI models (only needed once, ~5–10 seconds total)

```bash
python ai/train_toxicity.py
python ai/train_phishing.py
```

Both scripts print the **accuracy, confusion matrix, classification report,
and feature weights** — keep this output for your project report.

### 4. Seed demo users

```bash
python seed.py
```

Creates three accounts:

| Username | Password      | Role  |
|----------|---------------|-------|
| admin    | admin123      | admin |
| alice    | password123   | user  |
| bob      | password123   | user  |

### 5. Run the app

```bash
python app.py
```

Open `http://localhost:5000` in your browser.

---

## Demo script (use this in your viva)

1. Open Chrome → log in as **alice / password123** → you arrive in the room.
2. Open Edge or an incognito window → log in as **bob / password123** → you
   see alice's avatar; both can move with arrow keys / WASD.
3. **Clean message test** → alice types `Hello bob!` → bob sees it appear in
   chat. ✅
4. **Toxicity test** → alice types `you are so stupid get out of here` →
   a red toast pops up, bob sees nothing. The AI blocked it.
5. **Phishing test** → bob types `Check this http://paypal-verify-account.tk/login` →
   blocked as phishing.
6. **Clean URL test** → bob types `Check https://github.com` → goes through
   normally. ✅
7. Open a third browser tab → log in as **admin / admin123** → the dashboard
   shows the threats you just generated, with charts.
8. **Banning** → on `/admin/users`, click **Ban** next to alice → log back
   in as alice → blocked at login.

---

## How the AI works (1-minute viva summary)

### Toxicity model — `ai/train_toxicity.py`

- **Pipeline**: `TfidfVectorizer(ngram_range=(1,2), max_features=10000)` →
  `LogisticRegression(class_weight="balanced")`.
- **Why TF-IDF**: simple, interpretable, low memory, fast inference (<10 ms
  per message).
- **Why Logistic Regression**: probabilistic outputs (good for thresholds),
  coefficients are readable (you can print which words push a message
  toward "toxic").
- **Threshold**: 0.6 (configurable in `config.py`).

### Phishing-URL model — `ai/train_phishing.py`

- 16 hand-crafted URL features (length, dot count, `@` symbol, IP-as-host,
  HTTPS, suspicious keywords like *login/verify/secure*, risky TLDs like
  `.tk` / `.ml`, subdomain depth, …).
- `StandardScaler` → `LogisticRegression`.
- The training script prints **per-feature weights**, so you can tell the
  examiner *exactly which features the AI relies on*.

Both detectors are loaded once on first request (singleton pattern) so the
chat endpoint stays fast.

---

## Tech stack

- **Python 3.10+**, Flask, Flask-SQLAlchemy, Flask-Login
- **scikit-learn**, pandas, numpy, joblib
- **Bootstrap 5**, Chart.js (CDN)
- **SQLite** (file-based, zero setup)

No deep learning, no GPU, no paid APIs.

---

## Limitations & honest disclosure

- The bundled datasets are intentionally small (~390 rows each) so the
  whole project fits in one git repo. The same pipelines scale to the full
  Jigsaw Toxic Comment / PhishTank corpora.
- The "metaverse" is a 2D Canvas — VR / 3D was out of scope on purpose;
  the academic focus is the AI detection layer.
- Real-time chat uses HTTP polling (every 1 s), not WebSockets — sufficient
  for a 2-3 user demo.
- The threshold (0.6) is a tunable hyper-parameter; tighter thresholds
  reduce false positives, looser thresholds reduce false negatives.

---

## License

Educational use only. Built as an MCA final-year submission.
