from flask import Flask, send_from_directory

app = Flask(__name__)

FRONTEND_DIR = "frontend/html-css"

# Home
@app.route("/")
def home():
    return send_from_directory(f"{FRONTEND_DIR}/home", "index.html")

# Report Animal
@app.route("/report")
def report():
    return send_from_directory(f"{FRONTEND_DIR}/report-animal", "report.html")

# Rescue Dashboard
@app.route("/rescue")
def rescue():
    return send_from_directory(f"{FRONTEND_DIR}/rescue-dashboard", "rescue.html")

# Funding / Donate
@app.route("/funding")
def funding():
    return send_from_directory(f"{FRONTEND_DIR}/funding", "donate.html")

# About
@app.route("/about")
def about():
    return send_from_directory(f"{FRONTEND_DIR}/about", "about.html")

# Serve CSS from frontend
@app.route("/style.css")
def style():
    return send_from_directory(FRONTEND_DIR, "style.css")

if __name__ == "__main__":
    app.run(debug=True)
