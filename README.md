# 🐾 ViperAid — AI-Powered Animal Rescue & Shelter Management System

> Built for **PYEXPO 2026** | Project Code: **PY26006**

ViperAid is an AI-powered web application that bridges the gap between citizens and animal rescue organizations. It enables the public to report injured or stray animals using computer vision, connects them with nearby shelters, and gives NGO rescue teams a real-time dashboard to manage and respond to cases efficiently.

🌐 **Live Demo:** [https://vipheraid-deploy-7.onrender.com]

---

## ✨ Features

- 📸 **AI Animal Detection** — YOLOv8-powered image recognition identifies the animal species from a photo
- 🗺️ **GPS Location Tracking** — Reports are geotagged for accurate field dispatch
- 🚨 **Emergency Flagging** — Critical cases are marked and surfaced for immediate attention
- 🏠 **Shelter Directory** — Register, browse, and manage animal shelters with contact and capacity details
- 👥 **NGO Rescue Dashboard** — Dedicated login portal for rescue teams to view, assign, and resolve reports
- 📊 **Public Stats** — Live counters for total, active, and resolved animal rescue cases
- ☁️ **Cloud Database** — Supabase (PostgreSQL) for persistent, scalable data storage

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask 3.1 |
| Database | PostgreSQL (Supabase) / SQLite (local dev) |
| ORM | Flask-SQLAlchemy |
| AI Detection | YOLOv8 (Ultralytics 8.4) |
| Image Processing | Pillow, OpenCV |
| Frontend | HTML5, CSS3, JavaScript |
| Deployment | Render (via `Procfile`) |

---

## 📁 Project Structure

```
PY26006-main/
├── Procfile                    # Render deployment config
├── requirements.txt            # Python dependencies
├── Documentation/
│   ├── Demo.mp4
│   ├── Research_paper.pdf
│   ├── SOP.pdf
│   └── ppt.pdf
└── code/
    ├── app.py                  # Main Flask application
    ├── migrate_db.py           # Database migration helper
    ├── .env                    # Environment variables (do NOT commit)
    ├── .gitignore
    ├── yolov8n.pt              # YOLOv8 nano model weights
    ├── instance/
    │   └── viperaid.db         # Local SQLite database
    ├── static/
    │   ├── logo_cropped.png
    │   ├── qrcode.jpeg
    │   ├── style.css
    │   └── uploads/            # User-uploaded animal photos
    └── templates/
        ├── base.html
        ├── index.html
        ├── report.html
        ├── emergency.html
        ├── rescue.html
        ├── rescue-login.html
        ├── shelter.html
        └── donate.html
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.9+
- pip
- A [Supabase](https://supabase.com) account (free tier works)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/viperaid.git
cd viperaid/code
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file inside the `code/` folder:

```env
DATABASE_URL=postgresql://postgres:YourPassword@db.xxxx.supabase.co:5432/postgres
```

> For local development, you can omit this and the app will fall back to SQLite (`instance/viperaid.db`).

### 4. Run the app

```bash
python app.py
```

Open your browser at `http://127.0.0.1:5000`

---

## 🔐 NGO Rescue Login

Rescue teams can access the management dashboard at `/rescue-login`:

| Field | Value |
|---|---|
| Organization Name | Your NGO name |
| Access Code | `VIPERNGO` |

---

## 🌐 API Reference

### Reports

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/ai-report` | Submit a report with AI-analyzed photo |
| `GET` | `/api/reports` | Fetch all reports |
| `POST` | `/api/report` | Create a manual report |
| `POST` | `/api/report/<id>` | Update report status |
| `DELETE` | `/api/report/<id>` | Delete a report |

### Shelters

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/shelter` | Register a new shelter |
| `GET` | `/api/shelters` | Get all shelters |
| `PUT` | `/api/shelter/<id>` | Update shelter details |
| `DELETE` | `/api/shelter/<id>` | Remove a shelter |

### Utility

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/public-stats` | Get total / active / resolved counts |
| `POST` | `/api/detect-animal` | Run YOLOv8 detection on an uploaded image |

---

## 🗄️ Database Models

### `Report`
Stores citizen-submitted animal distress reports including GPS coordinates, AI-generated injury assessment, urgency level, status, and assigned rescue team.

### `Shelter`
Stores registered animal shelter information including name, type, address, capacity, operating hours, and animals accepted.

---

## 🔒 Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | Supabase PostgreSQL connection string |

---

## ☁️ Deployment

The project includes a `Procfile` for one-click deployment to [Render](https://render.com):

```
web: python code/app.py
```

Steps:
1. Push the repository to GitHub.
2. Create a new **Web Service** on Render, link the repo.
3. Set `DATABASE_URL` as an environment variable in Render's dashboard.
4. Deploy — Render will install dependencies and launch the server automatically.

---

## ⚠️ Security Notes

- **Never commit** your `.env` file — it's already listed in `.gitignore`
- **Never hardcode** your `GEMINI_KEY` in source files before pushing to GitHub
- The default NGO access code (`VIPERNGO`) should be changed before production deployment

---

## 📦 Key Dependencies

```bash
pip install flask flask-sqlalchemy psycopg2-binary python-dotenv \
            ultralytics pillow opencv-python
```

See `requirements.txt` for the full pinned dependency list.

---

## 🙌 Built With

- [Flask](https://flask.palletsprojects.com/) — Web framework
- [Supabase](https://supabase.com/) — Cloud PostgreSQL database
- [Ultralytics YOLOv8](https://ultralytics.com/) — Real-time object detection

---

## 📄 License

This project was developed for **PYEXPO 2026**. All rights reserved.