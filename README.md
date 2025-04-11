# 🏠 Household Services Application

A multi-user full-stack web application that enables **admins**, **customers**, and **service providers** to manage and deliver home services efficiently. Built as part of a college project with RESTful API support, user authentication, and admin control.

---

## 👨‍💻 Contributors

- [Niraj Kumar](https://github.com/nirajkumar1002)

---
## 🎥 Demo Video

📺 [Watch Demo](https://drive.google.com/file/d/1bXiD-rtTvE9WzJ4nRdJqX6gQkf1T_W7T/view)

---


## 🚀 Features

- Admin dashboard for managing services and users  
- Customer interface to view and request services  
- Service provider portal to accept and fulfill requests  
- User authentication and role-based access  
- Background task management with Celery & Redis

---

## 🛠️ Tech Stack

| Category         | Technology                              |
|------------------|------------------------------------------|
| **Frontend**     | Vue3 (CLI), Bootstrap                    |
| **Backend**      | Flask (REST API), SQLite, Redis, Celery  |
| **Languages**    | Python, JavaScript, HTML/CSS             |
| **Tools**        | Git, Postman, VS Code                    |

---

## 📂 Project Structure

project/ ├── frontend/ # Vue3 frontend ├── backend/ # Flask backend │ ├── api/ # API routes │ ├── celery_worker.py # Background task worker │ └── app.py # Main Flask app └── README.md


---

## ⚙️ How to Run

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/nirajkumar1002/household-services-app.git
cd household-services-app

### 2️⃣ Backend Setup
cd backend
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python app.py

### 3️⃣ Start Celery Worker (in a new terminal)
celery -A celery_worker.celery worker --loglevel=info

### 4️⃣ Frontend Setup
cd frontend
npm install
npm run serve

📌 Notes
The backend runs on http://localhost:5000

The frontend runs on http://localhost:8080

Use Postman or the frontend UI to test APIs and flows


## 📄 License

This project is intended for educational and academic purposes only.  
Reproduction, distribution, or commercial use of any part of this project is not permitted without explicit permission from the author.


