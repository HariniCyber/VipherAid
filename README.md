# 🐾 ViperAid — AI-Powered Animal Rescue & Shelter Management System

> Built for **PYEXPO 2026** | Project Code: **PY26006** | 🏆 Best UI/UX Award, PyExpo 2K26 Hackathon

ViperAid is an AI-powered web application that bridges the gap between citizens and animal rescue organizations. It enables the public to report injured or stray animals using computer vision, connects them with nearby shelters, and gives NGO rescue teams a real-time dashboard to manage and respond to cases efficiently.

🌐 **Live Demo:** [vipheraid-deploy-7.onrender.com](https://vipheraid-deploy-7.onrender.com)

---

## 👑 Leadership & Project Roles

**HariniCyber (Team Lead)**: Architected the core system layout, managed development pipelines, integrated the AI runtime architecture, and built deployment configurations.

---

## ✨ Features

- 📸 **AI Animal Detection**: YOLOv8-powered image recognition identifies the animal species from a photo
- 🗺️ **GPS Location Tracking**: Reports are geotagged for accurate field dispatch
- 🚨 **Emergency Flagging**: Critical cases are marked and surfaced for immediate attention
- 🏠 **Shelter Directory**: Register, browse, and manage animal shelters with contact and capacity details
- 👥 **NGO Rescue Dashboard**: Dedicated login portal for rescue teams to view, assign, and resolve reports
- 📊 **Public Stats**: Live counters for total, active, and resolved animal rescue cases
- ☁️ **Cloud Database**: Supabase (PostgreSQL) for persistent, scalable data storage

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
ViperAid/
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
    ├── .gitignore
    ├── yolov8n.pt              # YOLOv8 nano model weights
    ├── static/
    │   ├── logo_cropped.png
    │   ├── qrcode.jpeg
    │   └── style.css
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

> `.env`, the local SQLite database, and uploaded animal photos are created locally and are excluded from the repository by `.gitignore`.

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.9+
- pip
- A [Supabase](https://supabase.com) account (free tier works)

### 1. Clone the repository

```bash
git clone https://github.com/HariniCyber/ViperAid.git
cd ViperAid/code
```

### 2. Install dependencies

```bash
pip install -r ../requirements.txt
```

### 3. Configure environment variables

Create a `.env` file inside the `code/` folder:

```env
DATABASE_URL=postgresql://postgres:YourPassword@db.xxxx.supabase.co:5432/postgres
NGO_ACCESS_CODE=choose-your-own-strong-code
```

> For local development, you can omit `DATABASE_URL` and the app will fall back to SQLite.

### 4. Run the app

```bash
python app.py
```

Open your browser at `http://127.0.0.1:5000`

---

## 🔐 NGO Rescue Login

Rescue teams sign in at `/rescue-login` with their organization name and an access code. The access code is set by the administrator through the `NGO_ACCESS_CODE` environment variable and is never stored in the repository.

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
| `NGO_ACCESS_CODE` | Access code for the NGO rescue dashboard |

---

## ☁️ Deployment

The project includes a `Procfile` for deployment to [Render](https://render.com):

```
web: python code/app.py
```

Steps:
1. Push the repository to GitHub.
2. Create a new **Web Service** on Render and link the repo.
3. Set `DATABASE_URL` and `NGO_ACCESS_CODE` as environment variables in Render's dashboard.
4. Deploy. Render installs the dependencies and launches the server.

---

## ⚠️ Security Notes

- Never commit your `.env` file; it is listed in `.gitignore`.
- Never hardcode API keys, database passwords or access codes in source files.
- Use a strong, unique `NGO_ACCESS_CODE` and change it if it is ever exposed.

---

## 🙌 Built With

- [Flask](https://flask.palletsprojects.com/): web framework
- [Supabase](https://supabase.com/): cloud PostgreSQL database
- [Ultralytics YOLOv8](https://ultralytics.com/): real-time object detection

---

## 📄 License

This project was developed for **PYEXPO 2026**. All rights reserved.
