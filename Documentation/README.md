# 🐾 ViperAid — Animal Rescue & Shelter Management System

ViperAid is an AI-powered animal rescue web application built with Flask. It allows citizens to report injured or stray animals, locate nearby shelters, and enables NGO rescue teams to manage and respond to reports in real time.

---

## Deployment Link

(https://vipheraid-deploy-7.onrender.com/)


## 🚀 Features

- 📸 AI-powered animal detection using YOLOv8
- 🤖 Gemini AI for injury analysis and veterinary assessment
- 🗺️ GPS-based location tracking for reports
- 🏠 Shelter registration and management
- 🚨 Emergency report flagging
- 👥 NGO rescue team dashboard
- ☁️ Permanent cloud database using Supabase (PostgreSQL)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Database | PostgreSQL (Supabase) |
| ORM | Flask-SQLAlchemy |
| AI Detection | YOLOv8 (Ultralytics) |
| AI Analysis | Google Gemini 1.5 Flash |
| Frontend | HTML, CSS, JavaScript |

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/viperaid.git
cd viperaid/code
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

Create a `.env` file inside the `code` folder:
```
DATABASE_URL=postgresql://postgres:YourPassword@db.xxxx.supabase.co:5432/postgres
```

> Get your free database at [supabase.com](https://supabase.com)

### 4. Add your Gemini API Key

In `app.py`, replace:
```python
GEMINI_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

With your real key from [aistudio.google.com](https://aistudio.google.com)

### 5. Run the app
```bash
python app.py
```

Open your browser at:
```
http://127.0.0.1:5000
```

---

## 🔐 NGO Login

To access the rescue dashboard:

- Go to `/rescue-login`
- Enter your organization name
- Use code: `VIPERNGO`

---

## 📁 Project Structure
```
code/
├── app.py                  # Main Flask application
├── .env                    # Environment variables (never commit this!)
├── .gitignore              # Git ignore rules
├── yolov8n.pt              # YOLOv8 model weights
├── static/
│   └── uploads/            # Uploaded animal photos
└── templates/
    ├── index.html
    ├── report.html
    ├── emergency.html
    ├── rescue.html
    ├── rescue-login.html
    ├── shelter.html
    └── donate.html
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai-report` | Submit AI-analyzed animal report |
| GET | `/api/reports` | Get all reports |
| POST | `/api/report` | Create manual report |
| POST | `/api/report/<id>` | Update report status |
| DELETE | `/api/report/<id>` | Delete report |
| POST | `/api/shelter` | Register new shelter |
| GET | `/api/shelters` | Get all shelters |
| PUT | `/api/shelter/<id>` | Update shelter |
| DELETE | `/api/shelter/<id>` | Delete shelter |
| GET | `/api/public-stats` | Get total/active/resolved counts |
| POST | `/api/detect-animal` | Detect animal in image |

---

## 🔒 Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Supabase PostgreSQL connection string |

---

## ⚠️ Important Notes

- Never commit your `.env` file to GitHub
- Never commit your `GEMINI_KEY` to GitHub
- The `.gitignore` file already excludes `.env` and `*.db`

---

## 📦 Requirements

Install all dependencies with:
```bash
pip install flask flask-sqlalchemy psycopg2-binary python-dotenv ultralytics pillow google-generativeai
```

---

## 🙌 Built With

- [Flask](https://flask.palletsprojects.com/)
- [Supabase](https://supabase.com/)
- [Ultralytics YOLOv8](https://ultralytics.com/)
- [Google Gemini AI](https://aistudio.google.com/)

---

## 📄 License

This project was built for PYEXPO 2026. All rights reserved.