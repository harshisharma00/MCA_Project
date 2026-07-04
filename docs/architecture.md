# Architecture — MetaGuard

This document explains how the parts of the system fit together. Use it as
your viva cheat-sheet.

## 1. Layered view

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                      │
│  Bootstrap 5 templates · HTML5 Canvas room · Chart.js       │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP / fetch (JSON)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER (Flask)                 │
│   ┌──────────┐   ┌────────────────┐   ┌────────────────┐    │
│   │  auth    │   │  metaverse      │   │  admin         │   │
│   │ register │   │  /room          │   │ /admin         │   │
│   │ login    │   │  /api/chat/send │   │ /admin/threats │   │
│   │ logout   │   │  /api/positions │   │ /admin/users   │   │
│   └──────────┘   │  /api/move      │   │ /admin/api/    │   │
│                  └────────┬────────┘   │     stats      │   │
│                           │            └────────────────┘   │
│                  ┌────────▼─────────┐                       │
│                  │ AI / ML LAYER    │                       │
│                  │ ToxicityDetector │  TF-IDF + LogReg      │
│                  │ PhishingDetector │  features + LogReg    │
│                  └────────┬─────────┘                       │
└───────────────────────────┼─────────────────────────────────┘
                            │ ORM
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       DATA LAYER                            │
│  SQLite (instance/metaverse.db)                             │
│  Tables: users, messages, threats, urls_shared              │
└─────────────────────────────────────────────────────────────┘
```

## 2. Request flow — sending a chat message

```
[User types message]
        │
        ▼
[POST /api/chat/send  body: {content: "..."} ]
        │
        ▼
1. Toxicity check
   ToxicityDetector.predict(text) → (is_toxic, score)
        │
        ▼
2. URL extraction (regex in url_features.find_urls_in_text)
        │
        ▼
3. For each URL:
   PhishingDetector.predict(url) → (is_phishing, score)
   Insert into urls_shared
        │
        ▼
4. Insert into messages (is_threat=True if any flag fires)
   For each detection, insert into threats
        │
        ▼
5. Response:
   blocked == True    → red toast in UI, message NOT broadcast
   blocked == False   → next /api/messages poll picks it up,
                        every connected user sees it
```

## 3. Database schema

```
users
├── id (pk)
├── username (unique)
├── password_hash
├── role  (user | admin)
├── avatar_color
├── x, y                (position)
├── is_banned
└── created_at

messages
├── id (pk)
├── user_id (fk → users)
├── content
├── is_threat       ← if true, hidden from other users
├── threat_score
└── timestamp

threats
├── id (pk)
├── user_id (fk → users)
├── message_id (fk → messages, nullable)
├── threat_type    (toxicity | phishing)
├── score
├── payload        (offending text or URL)
└── timestamp

urls_shared
├── id (pk)
├── user_id (fk → users)
├── url
├── is_phishing
├── score
└── timestamp
```

## 4. AI models in detail

### Toxicity (text classification)

| Stage | Component |
|-------|-----------|
| Input | One chat message (string) |
| Vectoriser | `TfidfVectorizer(ngram_range=(1,2), max_features=10000, sublinear_tf=True)` |
| Classifier | `LogisticRegression(C=4.0, class_weight='balanced', solver='liblinear')` |
| Output | Probability of class **toxic**; threshold ≥ 0.6 → block |

### Phishing (URL classification)

| Stage | Component |
|-------|-----------|
| Input | One URL string |
| Feature extractor | 16 hand-crafted features (`ai/url_features.py`) |
| Scaler | `StandardScaler` |
| Classifier | `LogisticRegression(C=2.0, class_weight='balanced')` |
| Output | Probability of class **phishing**; threshold ≥ 0.6 → block |

The 16 features include URL/host/path lengths, counts of `.`/`-`/`@`/`?`/`=`,
the presence of an `@`, whether the host is an IP, HTTPS use, count of
suspicious keywords (`login`, `verify`, `bank`, `secure`, `update`, …),
risky TLDs (`.tk`, `.ml`, `.ga`, `.cf`, `.xyz`, …), digits in host, and
subdomain depth.

## 5. Why these design choices?

| Choice | Why |
|--------|-----|
| Flask (not Django) | Smaller, easier to read for a viva, perfect for a microservice-style ML app |
| SQLite (not Postgres) | Zero-setup; the whole DB is one file the examiner can inspect |
| Logistic Regression (not BERT / LSTM) | Trains in seconds, runs anywhere, **interpretable** — you can show the actual coefficients in your report |
| Polling (not WebSockets) | Avoids `flask-socketio` complexity and works behind any firewall |
| 2D Canvas (not Three.js) | The project's contribution is the AI, not 3D graphics; a 2D room demonstrates the "multi-user metaverse" idea cleanly |
| Hand-crafted URL features (not deep models on URLs) | Each feature is something you can name and defend in the viva |
