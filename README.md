# VipherAid 🐾

VipherAid is a web-based application built to centralize and streamline animal rescue efforts by connecting citizens, rescuers, NGOs, shelters, and veterinary doctors on a single platform.

---

## 🚨 Problem Statement

Animal rescue operations are currently fragmented and unorganized. Most rescue requests are shared through WhatsApp groups or informal networks, which leads to:

- Rescue cases getting lost or forgotten
- Rescuers being overwhelmed by unstructured information
- No proper tracking of rescue progress
- Lack of transparency for people willing to support rescues financially

---

## 💡 Solution

VipherAid provides a centralized system that organizes the entire rescue workflow. It allows:

- Citizens to report injured or distressed animals with verified information
- Rescuers, NGOs, and vets to manage and update rescue cases
- Transparent tracking of rescue status from report to resolution
- A structured way for people to support rescue efforts through a funding module (prototype)

---

## 🔄 Application Flow

1. **Home Page**  
   Acts as the entry point and redirects users to all main sections of the application.

2. **Report Animal**  
   Citizens submit:
   - Animal type  
   - Location  
   - Description of the issue  
   - Mandatory photo for verification  

3. **Rescue Dashboard**  
   Rescuers / NGOs / vets can:
   - View all reported cases  
   - Accept cases  
   - Update rescue status (Reported → In Progress → Resolved)

4. **Funding Section**  
   - Displays rescue cases that require financial support  
   - Shows purpose and estimated amount  
   - QR-based donation demo for hackathon purposes  

5. **About Page**  
   - Project overview  
   - Team details  

---

## 📁 Project Structure

The repository is organized to support parallel team collaboration and clean separation of concerns.

VipherAid/
├── frontend/
│ └── html-css/
│ ├── home/
│ │ └── index.html
│ ├── report-animal/
│ │ └── report.html
│ ├── rescue-dashboard/
│ │ └── rescue.html
│ ├── funding/
│ │ └── donate.html
│ └── about/
│ └── about.html
│
├── backend/
│ ├── app.py
│ ├── templates/
│ └── static/
│
├── presentation/
├── research/
├── .gitignore
└── README.md 


### Folder Explanation

- **frontend/**  
  Contains the static HTML and CSS files used by the frontend team to design and iterate on UI and UX.

- **backend/**  
  Contains the Flask application used to run the working demo and handle routing and future backend logic.

  - `app.py` – Flask entry point and route definitions  
  - `templates/` – Flask-rendered HTML pages  
  - `static/` – CSS and static assets  

- **presentation/**  
  Contains project presentation materials and scripts.

- **research/**  
  Contains research notes, references, and supporting information.

---

## 🛠 Tech Stack

### Frontend
- HTML
- CSS

### Backend
- Python
- Flask (for routing and application logic)

### Version Control
- Git
- GitHub

---

## 🎯 Project Aim

VipherAid aims to transform scattered and chaotic animal rescue efforts into a structured, transparent, and efficient system by leveraging web technologies and clear workflows. The project focuses on demonstrating a practical working model that can be expanded into a full-scale solution in the future.

---

## 📌 Note

This project is developed as a **hackathon prototype** to showcase concept feasibility, application flow, and technical implementation.

