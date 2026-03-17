from flask import Flask, render_template, request, redirect, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from ultralytics import YOLO
from PIL import Image

from google import genai
from google.genai import types

import os
import json
import base64
import io
import uuid
import math
app = Flask(__name__)
app.secret_key = "vipheraid_expo_final_2026_madurai"

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://neondb_owner:npg_ITNU4Oc2EQfd@ep-billowing-unit-amvksfur-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "connect_args": {"sslmode": "require", "connect_timeout": 10}
}
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db = SQLAlchemy(app)

# ── YOLO model ──
yolo_model = YOLO("yolov8n.pt")

# ── Gemini setup ──
GEMINI_KEY = "AIzaSyD38b-cJilMy3jevhOuHbfSC6yBxi8g70c"
client = genai.Client(api_key=GEMINI_KEY)

ANIMAL_CLASSES = [
    "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe"
]


# ───────────────── DATABASE MODELS ─────────────────
class Report(db.Model):
    id             = db.Column(db.String(40),  primary_key=True)
    created_at     = db.Column(db.DateTime,    default=datetime.utcnow)
    animal_type    = db.Column(db.String(50))
    breed          = db.Column(db.String(100))
    injury         = db.Column(db.String(200))
    severity       = db.Column(db.String(50))
    urgency        = db.Column(db.String(20),  default="Medium")
    location_text  = db.Column(db.String(200))
    geo            = db.Column(db.String(100))
    description    = db.Column(db.Text)
    reporter_name  = db.Column(db.String(100))
    reporter_phone = db.Column(db.String(20))
    status         = db.Column(db.String(20),  default="Reported")
    assigned_to    = db.Column(db.String(100))
    photo_url      = db.Column(db.String(300))
    latitude       = db.Column(db.Float)
    longitude      = db.Column(db.Float)
    is_emergency   = db.Column(db.Boolean,     default=False)


class Shelter(db.Model):
    id             = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    created_at     = db.Column(db.DateTime,    default=datetime.utcnow)
    name           = db.Column(db.String(200), nullable=False)
    shelter_type   = db.Column(db.String(50))
    address        = db.Column(db.String(300))
    city           = db.Column(db.String(100))
    phone          = db.Column(db.String(30))
    email          = db.Column(db.String(100))
    geo            = db.Column(db.String(100))
    capacity       = db.Column(db.String(20))
    animals_helped = db.Column(db.String(200))
    description    = db.Column(db.Text)
    hours          = db.Column(db.String(100))
    website        = db.Column(db.String(200))


with app.app_context():
    try:
        db.create_all()
        print("✅ Database connected and tables ready.")
    except Exception as e:
        print(f"⚠️ DB connection failed at startup: {e}")


# ───────────────── HELPER ─────────────────
def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two GPS coordinates."""
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ───────────────── PAGES ─────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/emergency")
def emergency():
    return render_template("emergency.html")

@app.route("/rescue")
def rescue():
    if not session.get("rescuer"):
        return redirect("/rescue-login")
    return render_template("rescue.html")

@app.route("/donate")
def donate():
    return render_template("donate.html")

@app.route("/shelter")
def shelter_page():
    return render_template("shelter.html")


# ───────────────── AUTH ─────────────────
@app.route("/rescue-login", methods=["GET", "POST"])
def rescue_login():
    if request.method == "POST":
        org  = request.form.get("org",  "").strip()
        code = request.form.get("code", "").strip()
        if code == "VIPERNGO":
            session["rescuer"] = True
            session["org"]     = org or "NGO"
            return redirect("/rescue")
        flash("Invalid NGO code. Try: VIPERNGO")
        return redirect("/rescue-login")
    return render_template("rescue-login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ───────────────── NEARBY SHELTERS API ─────────────────
@app.route("/api/nearby-shelters")
def api_nearby_shelters():
    try:
        lat    = request.args.get("lat",    type=float)
        lng    = request.args.get("lng",    type=float)
        radius = request.args.get("radius", default=50, type=float)

        if lat is None or lng is None:
            return jsonify({"error": "lat and lng are required"}), 400

        shelters = Shelter.query.all()
        nearby   = []

        for s in shelters:
            if not s.geo:
                continue
            try:
                parts = s.geo.split(",")
                s_lat = float(parts[0].strip())
                s_lng = float(parts[1].strip())
            except Exception:
                continue

            dist = haversine(lat, lng, s_lat, s_lng)
            if dist <= radius:
                nearby.append({
                    "id":             s.id,
                    "name":           s.name,
                    "shelter_type":   s.shelter_type,
                    "address":        s.address,
                    "city":           s.city,
                    "phone":          s.phone,
                    "email":          s.email,
                    "hours":          s.hours,
                    "animals_helped": s.animals_helped,
                    "distance_km":    round(dist, 1)
                })

        nearby.sort(key=lambda x: x["distance_km"])
        return jsonify({"shelters": nearby})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ───────────────── AI REPORT API ─────────────────
@app.route("/api/ai-report", methods=["POST"])
def ai_report():
    try:
        photo = request.files.get("photo")
        if not photo:
            return jsonify({"success": False, "error": "No photo uploaded"}), 400

        filename = f"{uuid.uuid4().hex}.jpg"
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        photo.save(path)

        # YOLO detection
        image = Image.open(path).convert("RGB")
        results = yolo_model(image)
        detected_animal = "Unknown"
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                detected_animal = yolo_model.names.get(cls, "Unknown")
                break

        # Gemini vision analysis
        prompt = """You are a veterinary assistant. Look at this animal image carefully.
Analyze the animal and return ONLY a valid JSON object — no extra text, no markdown, no backticks:
{
  "animal_type": "type of animal you see",
  "breed": "best guess at the breed",
  "injury": "describe visible injuries, or write None if the animal looks healthy",
  "severity": "one of: Low, Moderate, Severe, Critical",
  "urgency": "one of: Low, Medium, High, Emergency",
  "description": "2-3 sentences summarizing the animal condition and recommended action"
}"""

        try:
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="JPEG")
            img_bytes = img_byte_arr.getvalue()

            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-04-17",
                contents=[
                    types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
                    types.Part.from_text(text=prompt)
                ]
            )

            ai_text = response.text.strip()

            if "```" in ai_text:
                ai_text = ai_text.split("```")[1]
                if ai_text.lower().startswith("json"):
                    ai_text = ai_text[4:]
            ai_text = ai_text.strip()
            ai_data = json.loads(ai_text)

        except Exception as gemini_err:
            ai_data = {
                "animal_type": detected_animal,
                "breed":       "Unknown",
                "injury":      "Could not analyze image",
                "severity":    "Unknown",
                "urgency":     "Medium",
                "description": f"Gemini error: {str(gemini_err)}"
            }

        latitude  = request.form.get("latitude",  type=float)
        longitude = request.form.get("longitude", type=float)
        geo       = f"{latitude},{longitude}" if latitude and longitude else None
        report_id = "VA" + uuid.uuid4().hex[:10].upper()

        new_report = Report(
            id          = report_id,
            animal_type = ai_data.get("animal_type", detected_animal),
            breed       = ai_data.get("breed",       "Unknown"),
            injury      = ai_data.get("injury",      "Unknown"),
            severity    = ai_data.get("severity",    "Unknown"),
            urgency     = ai_data.get("urgency",     "Medium"),
            description = ai_data.get("description", "No description"),
            photo_url   = f"/static/uploads/{filename}",
            latitude    = latitude,
            longitude   = longitude,
            geo         = geo,
            status      = "Reported",
            assigned_to = ""
        )
        db.session.add(new_report)
        db.session.commit()

        return jsonify({
            "success":     True,
            "id":          new_report.id,
            "animal":      new_report.animal_type,
            "breed":       new_report.breed,
            "injury":      new_report.injury,
            "severity":    new_report.severity,
            "urgency":     new_report.urgency,
            "description": new_report.description,
            "photoUrl":    new_report.photo_url,
            "latitude":    new_report.latitude,
            "longitude":   new_report.longitude
        })

    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500


# ───────────────── REPORT APIs ─────────────────
@app.route("/api/report", methods=["POST"])
def api_create_report():
    if request.is_json:
        data  = request.json or {}
        photo = None
    else:
        data  = request.form.to_dict()
        photo = request.files.get("photo")

    photo_url = None
    if photo and photo.filename:
        filename  = secure_filename(f"{uuid.uuid4().hex}_{photo.filename}")
        photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        photo_url = f"/static/uploads/{filename}"

    is_emerg = str(data.get("isEmergency", "")).lower() in ("true", "1", "yes")

    r = Report(
        id             = "VA" + uuid.uuid4().hex[:10].upper(),
        animal_type    = data.get("animalType"),
        urgency        = data.get("urgency", "Medium"),
        location_text  = data.get("locationText"),
        geo            = data.get("geo"),
        description    = data.get("description"),
        reporter_name  = data.get("reporterName") or session.get("citizen_name"),
        reporter_phone = data.get("reporterPhone") or session.get("citizen_phone"),
        status         = "Reported",
        assigned_to    = "",
        photo_url      = photo_url,
        is_emergency   = is_emerg
    )
    db.session.add(r)
    db.session.commit()
    return jsonify({"success": True, "id": r.id, "photoUrl": photo_url})


@app.route("/api/reports")
def api_reports():
    reports = Report.query.order_by(
        Report.is_emergency.desc(),
        Report.created_at.desc()
    ).limit(100).all()

    return jsonify([{
        "id":            r.id,
        "animalType":    r.animal_type,
        "breed":         r.breed,
        "injury":        r.injury,
        "severity":      r.severity,
        "urgency":       r.urgency,
        "locationText":  r.location_text,
        "geo":           r.geo,
        "description":   r.description,
        "status":        r.status,
        "assignedTo":    r.assigned_to,
        "photoUrl":      r.photo_url,
        "isEmergency":   bool(r.is_emergency),
        "reporterName":  r.reporter_name,
        "reporterPhone": r.reporter_phone,
        "latitude":      r.latitude,
        "longitude":     r.longitude,
        "createdAt":     r.created_at.isoformat()
    } for r in reports])


@app.route("/api/report/<report_id>", methods=["POST"])
def api_update_report(report_id):
    if not session.get("rescuer"):
        return jsonify({"error": "Unauthorized"}), 403
    r    = Report.query.get_or_404(report_id)
    data = request.json or {}
    if "status"     in data: r.status      = data["status"]
    if "assignedTo" in data: r.assigned_to = data["assignedTo"]
    db.session.commit()
    return jsonify({"success": True})


@app.route("/api/report/<report_id>", methods=["DELETE"])
def api_delete_report(report_id):
    if not session.get("rescuer"):
        return jsonify({"error": "Unauthorized"}), 403
    r = Report.query.get_or_404(report_id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({"success": True})


# ───────────────── SHELTER APIs ─────────────────
@app.route("/api/shelter", methods=["POST"])
def api_create_shelter():
    data = request.json or {}
    s = Shelter(
        name           = data.get("name"),
        shelter_type   = data.get("shelter_type"),
        address        = data.get("address"),
        city           = data.get("city"),
        phone          = data.get("phone"),
        email          = data.get("email"),
        geo            = data.get("geo"),
        capacity       = data.get("capacity"),
        animals_helped = data.get("animals_helped"),
        description    = data.get("description"),
        hours          = data.get("hours"),
        website        = data.get("website")
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({"success": True, "id": s.id})


@app.route("/api/shelters")
def api_get_shelters():
    shelters = Shelter.query.order_by(Shelter.created_at.desc()).all()
    return jsonify([{
        "id":             s.id,
        "name":           s.name,
        "shelter_type":   s.shelter_type,
        "address":        s.address,
        "city":           s.city,
        "phone":          s.phone,
        "email":          s.email,
        "geo":            s.geo,
        "capacity":       s.capacity,
        "animals_helped": s.animals_helped,
        "description":    s.description,
        "hours":          s.hours,
        "website":        s.website
    } for s in shelters])


@app.route("/api/shelter/<int:shelter_id>", methods=["PUT"])
def api_update_shelter(shelter_id):
    shelter = Shelter.query.get_or_404(shelter_id)
    data    = request.json or {}
    shelter.name           = data.get("name",           shelter.name)
    shelter.shelter_type   = data.get("shelter_type",   shelter.shelter_type)
    shelter.address        = data.get("address",        shelter.address)
    shelter.city           = data.get("city",           shelter.city)
    shelter.phone          = data.get("phone",          shelter.phone)
    shelter.email          = data.get("email",          shelter.email)
    shelter.geo            = data.get("geo",            shelter.geo)
    shelter.capacity       = data.get("capacity",       shelter.capacity)
    shelter.animals_helped = data.get("animals_helped", shelter.animals_helped)
    shelter.description    = data.get("description",    shelter.description)
    shelter.hours          = data.get("hours",          shelter.hours)
    shelter.website        = data.get("website",        shelter.website)
    db.session.commit()
    return jsonify({"success": True, "id": shelter.id})


@app.route("/api/shelter/<int:shelter_id>", methods=["DELETE"])
def api_delete_shelter(shelter_id):
    shelter = Shelter.query.get_or_404(shelter_id)
    db.session.delete(shelter)
    db.session.commit()
    return jsonify({"success": True})


# ───────────────── AI ANIMAL DETECTION ─────────────────
@app.route("/api/detect-animal", methods=["POST"])
def api_detect_animal():
    data      = request.json or {}
    image_b64 = data.get("image", "")

    if not image_b64:
        return jsonify({"isAnimal": False})

    try:
        image_bytes = base64.b64decode(image_b64)
        image       = Image.open(io.BytesIO(image_bytes))
        results     = yolo_model(image)

        for r in results:
            for box in r.boxes:
                cls   = int(box.cls[0])
                label = yolo_model.names[cls]
                if label in ANIMAL_CLASSES:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    bbox = {
                        "x":      x1 / image.width,
                        "y":      y1 / image.height,
                        "width":  (x2 - x1) / image.width,
                        "height": (y2 - y1) / image.height
                    }
                    return jsonify({
                        "isAnimal":   True,
                        "animalType": label,
                        "bbox":       bbox
                    })

        return jsonify({"isAnimal": False, "detectedAs": "No animal detected"})

    except Exception as e:
        return jsonify({"isAnimal": False, "detectedAs": "AI error"})


# ───────────────── MISC ─────────────────
@app.route("/favicon.ico")
def favicon():
    return "", 204


@app.route("/api/public-stats")
def api_public_stats():
    total    = Report.query.count()
    resolved = Report.query.filter_by(status="Completed").count()
    active   = Report.query.filter(Report.status != "Completed").count()
    return jsonify({"total": total, "resolved": resolved, "active": active})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)