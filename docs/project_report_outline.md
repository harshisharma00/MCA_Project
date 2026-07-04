# Project Report Outline — MetaGuard

A chapter-by-chapter outline you can copy into your college report template.
Lengths are rough page-count guidance for an MCA submission.

## Front matter

- Cover page (title, name, roll number, supervisor, university, year)
- Certificate
- Declaration
- Acknowledgements
- Abstract (1 page)
- Table of contents
- List of figures
- List of tables

---

## Chapter 1 — Introduction (4–6 pages)

1.1 Background — what is the metaverse, why is it growing
1.2 Common metaverse-specific threats
   - Avatar harassment / hate speech in voice & text chat
   - Phishing links shared in chat / NFT scams
   - Account takeover and impersonation
   - Bot-controlled avatars
1.3 Motivation — why automated AI moderation is needed
1.4 Problem statement
1.5 Objectives of the project
1.6 Scope and limitations
1.7 Organisation of the report

## Chapter 2 — Literature Review (5–8 pages)

2.1 Online toxicity detection — history (rule-based filters → ML → deep
   learning), Jigsaw / Perspective API, prior work
2.2 Phishing URL detection — feature-engineering approaches, lexical vs
   network features
2.3 Trust & safety in virtual worlds — Roblox, VRChat, Meta Horizon Worlds
   case studies
2.4 Gaps in existing solutions that this project addresses

## Chapter 3 — System Analysis (4–6 pages)

3.1 Existing system (manual moderation, blocked-word lists)
3.2 Limitations of the existing system
3.3 Proposed system — automated AI threat detection
3.4 Feasibility study (technical, operational, economic)
3.5 Hardware & software requirements

## Chapter 4 — System Design (6–10 pages)

4.1 System architecture (use the diagram from `docs/architecture.md`)
4.2 Module description
   - Authentication module
   - Metaverse room / chat module
   - AI detection module (toxicity + phishing)
   - Admin / moderation module
4.3 Data Flow Diagrams (DFD level 0, level 1)
4.4 ER Diagram (use the schema in `architecture.md`)
4.5 UML diagrams
   - Use case diagram (User, Admin)
   - Sequence diagram for "send chat message" flow
   - Class diagram for SQLAlchemy models
4.6 Database schema description (each table, columns, types, constraints)

## Chapter 5 — Implementation (8–12 pages)

5.1 Tools & technologies — Python, Flask, SQLAlchemy, scikit-learn, Bootstrap
5.2 Folder structure (paste from README)
5.3 Backend — Flask app factory + blueprints, with code excerpts
5.4 AI / ML implementation
   - Dataset preparation
   - Toxicity pipeline (TF-IDF + Logistic Regression) — paste training code
   - Phishing pipeline (feature engineering + Logistic Regression)
5.5 Frontend — Bootstrap layout, HTML5 Canvas avatar rendering, chat UI
5.6 Database — SQLite, models, migrations
5.7 Admin dashboard — Chart.js integration

## Chapter 6 — Testing & Results (6–8 pages)

6.1 Testing approach
   - Unit tests (manual) for AI predictions
   - Integration tests (manual) for end-to-end flow
   - User acceptance test scenarios
6.2 Toxicity model results
   - Confusion matrix (paste from training output)
   - Accuracy / precision / recall / F1
   - ROC curve (optional)
6.3 Phishing model results
   - Confusion matrix
   - Top-weighted features
6.4 Sample screenshots
   - Login page
   - Metaverse room with avatars
   - Toxic message blocked (red toast)
   - Phishing URL blocked
   - Admin dashboard with charts
   - User management page
6.5 Performance — average response time, model size

## Chapter 7 — Conclusion & Future Scope (2–3 pages)

7.1 Summary of work done
7.2 Achievements — what objectives were met
7.3 Limitations — small dataset, 2D simulation, polling vs WebSockets
7.4 Future scope
   - Deep-learning toxicity (DistilBERT) for nuanced cases
   - Real-time WebSockets
   - Voice-chat moderation (audio → text → toxicity)
   - 3D / VR room using Three.js or Unity
   - Image-based avatar moderation
   - Behavioural anomaly detection (login patterns, action frequency)

## References / Bibliography

Use IEEE / APA format as your university requires. Sample seed entries:

- Wulczyn, E., Thain, N., & Dixon, L. (2017). *Ex Machina: Personal Attacks
  Seen at Scale*. WWW 2017.
- Mohammad, R. M., et al. (2014). *Predicting Phishing Websites Based on
  Self-Structuring Neural Network*. Neural Computing and Applications.
- Mozur, P. (2022). *The Metaverse Has Bullies, Trolls and Pirates*.
  The New York Times.
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.
- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python*.
  JMLR 12.

## Appendices

A. Source code listings (key files only — auth.py, metaverse.py, train_*.py)
B. Sample data — first 20 rows of each CSV
C. Screenshots index
D. Installation & run instructions (paste from README)
