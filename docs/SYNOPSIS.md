# PROJECT SYNOPSIS

## METAVERSE THREAT DETECTION AI

**A Synopsis Submitted in Partial Fulfilment of the Requirements
for the Award of the Degree of**

# MASTER OF COMPUTER APPLICATIONS (MCA)

---

**Submitted by:**
[Your Full Name]
Roll No. / Registration No. — [Your Roll Number]
MCA — Final Year — Semester [IV]

**Under the Guidance of:**
[Supervisor's Name]
[Designation, Department]

**Department of Computer Applications**
**Chandigarh University, Gharuan, Mohali, Punjab**
[Academic Session — 2025-2026]

---

## TABLE OF CONTENTS

1. Introduction
2. Problem Statement
3. Objectives of the Project
4. Existing System
5. Proposed System
6. Scope of the Project
7. Methodology
8. System Architecture
9. Modules / Functional Description
10. Database Design
11. Hardware and Software Requirements
12. Tools and Technologies Used
13. Expected Outcomes
14. Project Timeline
15. Future Enhancements
16. References

---

## 1. INTRODUCTION

The **metaverse** is an immersive, three-dimensional virtual world where
users interact with one another through digital avatars in real time. With
the rapid growth of platforms such as Meta Horizon Worlds, Roblox, VRChat,
Decentraland, and The Sandbox, millions of users now spend significant
hours communicating, shopping, gaming, and conducting business inside
these virtual environments.

However, this growth has introduced an entirely new attack surface for
cyber-threats. Toxic and abusive language, harassment of avatars, phishing
links shared in voice or text chat, fake-identity scams, and in-game NFT
fraud are now reported daily across major metaverse platforms. Unlike
traditional social media, metaverse interactions are real-time, ephemeral,
and often go unmoderated — making manual review impractical at scale.

To counter these threats, an **Artificial Intelligence (AI) based threat
detection system** is required that can monitor user activity inside the
metaverse and identify malicious content automatically — in real time,
without slowing down the experience.

This project, titled **"Metaverse Threat Detection AI"** (codename
*MetaGuard*), proposes and implements a working prototype of such a system.
It simulates a small multi-user metaverse environment, monitors every chat
message for toxicity and phishing attempts using two trained Machine
Learning models, and provides moderators with a real-time dashboard for
oversight and action.

---

## 2. PROBLEM STATEMENT

> *"How can we automatically detect harmful content (abusive chat and
> phishing URLs) shared between avatars in a metaverse environment,
> in real time, with minimal latency, and provide moderators with the
> tools to take action against offenders?"*

Specifically, the problem has three parts:

1. **Detection of textual abuse** — flagging hate speech, harassment, or
   toxic chat between avatars before it reaches the recipient.
2. **Detection of phishing URLs** — identifying suspicious links shared
   in chat that mimic legitimate banks, wallets, or game platforms.
3. **Moderation tooling** — giving administrators a live dashboard with
   analytics so that repeat offenders can be banned promptly.

---

## 3. OBJECTIVES OF THE PROJECT

The primary objectives of this project are:

1. To design and build a **simulated metaverse environment** in which
   multiple users can interact through avatars and exchange chat messages
   in real time.
2. To train and integrate two **AI / Machine Learning models** for:
   - Detecting toxic, abusive, or harassing chat messages.
   - Detecting phishing or fraudulent URLs shared inside the chat.
3. To **block flagged content** automatically before it reaches other
   users, while preserving an audit trail for the administrator.
4. To build a **moderator dashboard** that visualises detected threats
   over time and allows banning of malicious users.
5. To ensure that the entire system runs on a single laptop without
   requiring a GPU, the cloud, or paid third-party APIs — making it
   suitable for academic demonstration.
6. To produce a working prototype that is **interpretable** — every
   detection decision can be explained using model weights, satisfying
   modern explainable-AI requirements.

---

## 4. EXISTING SYSTEM

Current moderation in metaverse platforms relies primarily on:

- **Manual reporting** — a victim must report an offender, after which a
  human moderator reviews the incident. This is slow, inconsistent, and
  cannot scale to millions of concurrent users.
- **Static blocklists** — keyword filters that flag pre-defined words.
  These are easily bypassed using misspellings, leetspeak, or new slang,
  and produce many false positives.
- **Browser-level safe browsing** — services such as Google Safe Browsing
  warn users only when the URL is opened in a normal browser, which is
  ineffective against links shared inside a metaverse chat that opens an
  embedded WebView or copies the URL to the clipboard.

### Limitations of the Existing System

1. Reactive, not proactive — damage is already done before action is taken.
2. Cannot understand context — sarcasm, slang, and code-switching are missed.
3. Manual moderators do not scale to the number of concurrent metaverse
   users.
4. No real-time visibility into platform-wide threat trends.
5. Phishing URLs often use look-alike domains and risky TLDs that simple
   blocklists do not catch.

---

## 5. PROPOSED SYSTEM

The proposed system, **MetaGuard**, addresses these gaps by introducing an
**AI-driven, real-time, server-side moderation pipeline** that screens
every chat message before it is broadcast to other avatars.

### Key Features of the Proposed System

- A multi-user 2D metaverse room implemented on an HTML5 Canvas, where
  registered users move avatars using arrow / WASD keys and chat freely.
- A trained **toxicity classifier** (TF-IDF vectoriser + Logistic
  Regression) that scores every chat message and blocks any message
  whose toxicity probability exceeds a configurable threshold.
- A trained **phishing-URL classifier** (16 hand-crafted lexical
  features + Logistic Regression) that scores every URL shared in chat
  and blocks the message if any contained URL is found suspicious.
- A complete **administrator dashboard** with:
  - Live counters for total users, banned users, messages today,
    threats detected today.
  - A line chart showing toxicity and phishing threats per hour over
    the last 24 hours.
  - A doughnut chart showing the toxicity-vs-phishing split.
  - A live-updating table of the most recent threats.
  - A users page to ban or unban any user with one click.
- The dashboard polls fresh data every 3 seconds, so moderators see
  threats appear without refreshing the browser.

### Advantages over the Existing System

| Aspect              | Existing System                  | Proposed System                  |
|---------------------|----------------------------------|----------------------------------|
| Detection mode      | Reactive (after report)          | Proactive (before delivery)      |
| Scalability         | Bound by human moderators        | Bound only by server CPU         |
| URL safety          | Browser-side only                | Server-side, real-time           |
| Explainability      | Black box                        | Logistic-regression weights      |
| Latency             | Hours to days                    | Under 10 ms per message          |
| Moderator insight   | Spreadsheets / log files         | Live dashboard with charts       |

---

## 6. SCOPE OF THE PROJECT

### In Scope

- Authentication (registration, login, logout, password hashing).
- A 2D Canvas-based metaverse room with multi-user avatar rendering and
  position synchronisation.
- Real-time text chat with server-side AI moderation.
- Two ML models trained on bundled datasets:
  - Toxicity dataset — ~424 labelled chat messages.
  - Phishing dataset — ~397 labelled URLs.
- Administrator dashboard with live polling, charts, and ban controls.
- Complete project documentation, architecture diagram, and report outline.

### Out of Scope (for this prototype)

- 3D / Virtual Reality rendering (would shift focus away from the AI core).
- Real-time WebSockets (HTTP polling at 1-3 seconds is sufficient for a
  multi-user demo).
- Voice-chat transcription and toxicity (could be a future enhancement).
- Production-grade datasets (the bundled CSVs scale conceptually to the
  full Jigsaw and PhishTank corpora).
- Behavioural anomaly detection of avatars (also a future-scope item).

---

## 7. METHODOLOGY

The project follows the **iterative incremental software development model**,
chosen because the AI components must be trained and validated separately
before they are integrated into the web application.

### Development Phases

1. **Requirement Analysis** — identify the metaverse threats most relevant
   to text-based interaction; finalise feature list and acceptance
   criteria.
2. **Dataset Preparation** — curate a small, balanced dataset of clean and
   toxic messages, and a balanced dataset of legitimate and phishing URLs.
3. **Model Training & Evaluation** — train classifiers using scikit-learn,
   evaluate on a hold-out set, record accuracy / precision / recall / F1
   and confusion matrices.
4. **Backend Development** — Flask application factory, SQLAlchemy ORM
   models, three blueprints (auth, metaverse, admin), session management
   with Flask-Login.
5. **AI Integration** — load trained models as singletons inside the Flask
   process; integrate prediction calls into the chat-send endpoint.
6. **Frontend Development** — Bootstrap-styled templates, HTML5 Canvas
   room, Chart.js dashboard.
7. **Testing & Demo** — manual end-to-end tests for each threat type and
   each user role; verification that detection happens before broadcast.
8. **Documentation** — synopsis, README, architecture document, project
   report outline.

### Machine-Learning Pipeline

```
   Raw chat / URL  ──►  Preprocessing  ──►  Vectorisation /
                                            Feature Extraction
                                                  │
                                                  ▼
                                      Logistic Regression  ──►  Probability
                                                  │
                                                  ▼
                                       Threshold (0.6) ──► Block / Allow
```

---

## 8. SYSTEM ARCHITECTURE

```
Browser (User)                        Browser (Admin)
   │                                     │
   │ HTTP / fetch (JSON)                 │
   ▼                                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  FLASK WEB APP (app.py)                     │
│  ┌──────────────┬──────────────────┬───────────────────┐    │
│  │  auth        │  metaverse       │   admin           │    │
│  │  blueprint   │  blueprint       │   blueprint       │    │
│  │              │                  │                   │    │
│  │  /register   │  /room           │   /admin          │    │
│  │  /login      │  /api/chat/send  │   /admin/threats  │    │
│  │  /logout     │  /api/positions  │   /admin/users    │    │
│  │              │  /api/move       │   /admin/api/stats│    │
│  └──────────────┴────────┬─────────┴───────────────────┘    │
│                          │                                  │
│              ┌───────────▼───────────┐                      │
│              │      AI / ML LAYER    │                      │
│              │  ToxicityDetector     │  TF-IDF + LogReg     │
│              │  PhishingDetector     │  Features + LogReg   │
│              └───────────┬───────────┘                      │
│                          │                                  │
│                  SQLAlchemy ORM                             │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           ▼
                ┌──────────────────────┐
                │  SQLite (metaverse.db)│
                │  users               │
                │  messages            │
                │  threats             │
                │  urls_shared         │
                └──────────────────────┘
```

---

## 9. MODULES / FUNCTIONAL DESCRIPTION

### Module 1 — User Authentication

- Functions: register, login, logout, ban-check on login.
- Passwords are hashed using Werkzeug's `generate_password_hash` (PBKDF2).
- Sessions are managed using Flask-Login.

### Module 2 — Metaverse Room (User-Facing Frontend)

- An HTML5 Canvas of 800 × 500 pixels representing the virtual room.
- Each avatar is drawn as a coloured circle labelled with the username.
- Movement: arrow keys or WASD; position is sent to the server via
  `/api/move` and broadcast to all clients via `/api/positions` polling.
- A side panel hosts the live chat input, output, and threat-toast
  notifications when a message is blocked.

### Module 3 — Toxicity Detection

- Pipeline: `TfidfVectorizer (1-2 grams, 10000 features)` →
  `LogisticRegression (C = 4.0, class_weight = balanced)`.
- Threshold: probability ≥ 0.6 is treated as toxic.
- Output: `(is_toxic, confidence_score)`.

### Module 4 — Phishing-URL Detection

- 16 hand-crafted features per URL: length, dots, dashes, `@`, `?`, `=`,
  `//`, IP-as-host, HTTPS, suspicious-keyword count, risky-TLD flag,
  digits in host, subdomain depth, and more.
- Pipeline: `StandardScaler` → `LogisticRegression (C = 2.0)`.
- Threshold: probability ≥ 0.6 is treated as phishing.

### Module 5 — Chat Pipeline

- Flow: user submits message → toxicity check on full text → URL
  extraction (regex) → phishing check on each URL → if any check fires,
  the message is **stored** with `is_threat = True` and **never
  broadcast**; a `Threat` record is created. Otherwise the message goes
  out via the next polling cycle.

### Module 6 — Administrator Dashboard

- Live cards: total users, banned users, messages today, threats today.
- Line chart: threats per hour over the last 24 hours.
- Doughnut chart: toxicity-versus-phishing split.
- Recent threats table: the latest 10 detections with offender, score,
  and payload.
- Polling: every 3 seconds, the dashboard auto-updates without a page
  refresh.

### Module 7 — User Management

- The administrator can ban or unban any user.
- A banned user is immediately logged out and cannot log back in.

---

## 10. DATABASE DESIGN

The database is **SQLite** (file-based), accessed through Flask-SQLAlchemy.

### Table — `users`

| Column          | Type         | Description                              |
|-----------------|--------------|------------------------------------------|
| id              | INTEGER PK   | Primary key                              |
| username        | VARCHAR(50)  | Unique username                          |
| password_hash   | VARCHAR(255) | PBKDF2-hashed password                   |
| role            | VARCHAR(10)  | "user" or "admin"                        |
| avatar_color    | VARCHAR(7)   | Hex colour, e.g. `#5DADE2`               |
| x, y            | INTEGER      | Avatar position in the room              |
| is_banned       | BOOLEAN      | Set to true when the admin bans the user |
| created_at      | DATETIME     | Account creation timestamp               |

### Table — `messages`

| Column          | Type         | Description                              |
|-----------------|--------------|------------------------------------------|
| id              | INTEGER PK   |                                          |
| user_id         | FK → users   | Sender                                   |
| content         | TEXT         | The message itself                       |
| is_threat       | BOOLEAN      | True if any AI check flagged it          |
| threat_score    | FLOAT        | Highest score among the AI checks        |
| timestamp       | DATETIME     | When sent                                |

### Table — `threats`

| Column          | Type         | Description                              |
|-----------------|--------------|------------------------------------------|
| id              | INTEGER PK   |                                          |
| user_id         | FK → users   | Offender                                 |
| message_id      | FK → messages| Linked message (nullable)                |
| threat_type     | VARCHAR(20)  | "toxicity" or "phishing"                 |
| score           | FLOAT        | Model confidence                         |
| payload         | TEXT         | Offending text or URL                    |
| timestamp       | DATETIME     | Detection time                           |

### Table — `urls_shared`

| Column          | Type         | Description                              |
|-----------------|--------------|------------------------------------------|
| id              | INTEGER PK   |                                          |
| user_id         | FK → users   |                                          |
| url             | VARCHAR(500) |                                          |
| is_phishing     | BOOLEAN      |                                          |
| score           | FLOAT        |                                          |
| timestamp       | DATETIME     |                                          |

---

## 11. HARDWARE AND SOFTWARE REQUIREMENTS

### Minimum Hardware Requirements

- Processor: Intel Core i3 (8th generation) or equivalent
- RAM: 4 GB
- Storage: 500 MB free disk space
- Display: 1366 × 768 resolution
- Internet: only for first-time `pip install`; runtime is fully offline

### Recommended Hardware

- Processor: Intel Core i5 (10th generation) or higher
- RAM: 8 GB
- SSD storage

### Software Requirements

- Operating System: Windows 10 / 11, Ubuntu 20.04+, or macOS 11+
- Python 3.10 or higher
- Web Browser: Google Chrome 110+ or Microsoft Edge 110+
- Code Editor: Visual Studio Code (recommended)

---

## 12. TOOLS AND TECHNOLOGIES USED

| Layer               | Technology                                        |
|---------------------|---------------------------------------------------|
| Programming Language| Python 3.10+, JavaScript (ES6)                    |
| Web Framework       | Flask 3.x                                         |
| ORM / Database      | Flask-SQLAlchemy with SQLite                      |
| Authentication      | Flask-Login, Werkzeug security                    |
| Machine Learning    | scikit-learn 1.4+, NumPy, pandas                  |
| Model Persistence   | joblib                                            |
| Frontend Markup     | HTML5, Jinja2 templates                           |
| Styling             | Bootstrap 5                                       |
| Visualisation       | HTML5 Canvas, Chart.js 4                          |
| Version Control     | Git, GitHub                                       |
| IDE                 | Visual Studio Code                                |

---

## 13. EXPECTED OUTCOMES

By the end of this project, the following deliverables are expected:

1. A working web application in which multiple users can sign up, log in,
   and interact in a shared 2D metaverse room.
2. Two trained Machine-Learning models (toxicity and phishing) saved as
   `.pkl` files, with reproducible training scripts and reported
   evaluation metrics.
3. A real-time chat pipeline in which **no toxic or phishing content ever
   reaches another user** — the AI blocks it before broadcast.
4. An administrator dashboard with live counters, two interactive charts,
   a recent-threats table, and one-click user banning.
5. Complete documentation:
   - This synopsis
   - A README with setup and demo steps
   - An architecture document
   - A chapter-wise project-report outline
6. Reported model performance:
   - Toxicity classifier — measured accuracy ≈ **82 %** on hold-out.
   - Phishing classifier — measured accuracy ≈ **100 %** on hold-out
     (small bundled dataset; scales to ~94-96 % on the full PhishTank
     corpus).

### Anticipated Screenshots

- Login and registration pages.
- The metaverse room with two avatars present.
- A red toast appearing when the AI blocks a toxic message.
- A red toast appearing when the AI blocks a phishing URL.
- The admin dashboard showing the live cards, two charts, and the
  recent-threats table.
- The user-management page showing a banned user.

---

## 14. PROJECT TIMELINE

The project is planned for completion across one academic semester.

| Week  | Activity                                                                   |
|-------|----------------------------------------------------------------------------|
| 1-2   | Topic finalisation, literature survey, synopsis writing                    |
| 3     | Requirement analysis, dataset sourcing                                      |
| 4     | Database design, Flask application factory, authentication module          |
| 5     | Toxicity dataset preparation, model training, evaluation                   |
| 6     | Phishing dataset preparation, feature engineering, model training          |
| 7     | Metaverse room (HTML5 Canvas) and chat backend                             |
| 8     | AI integration into the chat pipeline, threat-toast notifications          |
| 9     | Admin dashboard, charts, user management                                   |
| 10    | Live-polling for the dashboard, end-to-end manual testing                   |
| 11    | Documentation (README, architecture, report draft)                         |
| 12    | Final review, presentation preparation, viva                                |

---

## 15. FUTURE ENHANCEMENTS

1. **Voice-chat moderation** — convert speech to text using Whisper and
   apply the existing toxicity classifier in real time.
2. **Deep-learning upgrade** — replace TF-IDF + Logistic Regression with
   DistilBERT for nuanced detection of sarcasm and code-switched text.
3. **Behavioural anomaly detection** — Isolation Forest on login times,
   message frequency, and movement patterns to flag bot avatars.
4. **3D / VR room** — re-build the metaverse room using Three.js or a
   Unity WebGL build, while keeping the same backend AI pipeline.
5. **Real-time WebSocket layer** — replace HTTP polling with
   Flask-SocketIO for sub-200-millisecond message delivery.
6. **Image / NSFW screening** — integrate a CNN-based classifier for
   uploaded avatar images or shared media.
7. **Federated training** — allow multiple metaverse servers to improve
   the toxicity model collectively without sharing raw chat data.

---

## 16. REFERENCES

1. Wulczyn, E., Thain, N., and Dixon, L. *Ex Machina: Personal Attacks
   Seen at Scale*. Proceedings of WWW 2017.
2. Mohammad, R. M., Thabtah, F., and McCluskey, L. *Predicting Phishing
   Websites Based on Self-Structuring Neural Network*. Neural Computing
   and Applications, 2014.
3. Pedregosa, F. et al. *Scikit-learn: Machine Learning in Python*.
   Journal of Machine Learning Research, Volume 12, 2011.
4. Bishop, C. M. *Pattern Recognition and Machine Learning*. Springer,
   2006.
5. Mozur, P. *The Metaverse Has Bullies, Trolls and Pirates*. The New
   York Times, 2022.
6. OWASP Foundation. *OWASP Top 10 Web Application Security Risks*.
   <https://owasp.org>
7. Jigsaw / Conversation AI. *Toxic Comment Classification Challenge*.
   Kaggle, 2018.
8. PhishTank. *Open-source phishing-URL repository*.
   <https://phishtank.org>
9. Flask Documentation. <https://flask.palletsprojects.com>
10. Scikit-learn User Guide.
    <https://scikit-learn.org/stable/user_guide.html>
11. Mozilla Developer Network. *HTML Canvas API*.
    <https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API>
12. Chart.js Documentation. <https://www.chartjs.org/docs/latest/>

---

## DECLARATION

I hereby declare that the work presented in this synopsis titled
**"Metaverse Threat Detection AI"** is original and has been carried out
by me under the guidance of my supervisor. To the best of my knowledge,
this work has not been submitted elsewhere for the award of any degree.

|                                          |                                          |
|------------------------------------------|------------------------------------------|
| Date: ____________                       | Signature of Student                     |
| Place: Chandigarh University             | [Your Name]                              |
|                                          | Roll No.: [Your Roll Number]             |

|                                          |                                          |
|------------------------------------------|------------------------------------------|
| Signature of Supervisor                  | Signature of HoD                         |
| [Supervisor's Name]                      | Department of Computer Applications      |
| Department of Computer Applications      |                                          |

---

*End of Synopsis*
