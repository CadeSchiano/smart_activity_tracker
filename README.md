# 🚀 Smart Activity Tracker (Full-Stack AI App)

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/frontend-react-blue)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/backend-fastapi-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#license)

---

## 📌 Overview

**Smart Activity Tracker** is a full-stack AI-powered web application that allows users to create, manage, and analyze activities through a modern dashboard interface.

The application combines a **React frontend**, **FastAPI backend**, and an **LLM-powered assistant** to enable natural language interaction with user data.

---

## ✨ Features

### 🧩 Core Functionality
- Create, view, update, and delete activities (CRUD)
- Categorize activities (e.g., Fitness, School, Work)
- Persistent storage using SQLite + SQLAlchemy
- UUID-based activity identifiers

### 🤖 AI Integration
- Ask questions about your activities using natural language
- Generate summaries and insights
- Context-aware responses powered by LLM

### 🔐 Authentication (Planned Upgrade)
- Future implementation of user registration and login system
- Secure user-based activity tracking

### 🎨 Frontend (React)
- Modern dashboard UI
- Responsive layout
- Interactive components
- Real-time updates

### 🌐 Backend API
- RESTful API with FastAPI
- Automatic Swagger docs
- Structured data models with Pydantic

---

## 🛠️ Tech Stack

### Frontend
- React (Vite)
- JavaScript (ES6+)
- CSS (custom styling)

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy
- Uvicorn

### AI
- OpenAI API (LLM integration)

### Auth
- JWT (current implementation)
- Database-backed auth (planned)

### Database
- SQLite

### Testing
- Pytest

### Deployment
- Render (backend)
- Vercel (frontend — optional)

---

## 📁 Project Structure

```
smart_activity_tracker/
├── apps/
│   ├── api.py          # FastAPI routes
│   ├── core.py         # Business logic
│   ├── activity.py     # Data model
│   ├── database.py     # DB setup
│   └── ai.py           # AI integration
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx     # Main React component
│   │   ├── App.css     # Styling
│   │   └── main.jsx
│   └── package.json
│
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚡ Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/CadeSchiano/smart_activity_tracker.git
cd smart_activity_tracker
```

### 2. Backend setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run backend:

```bash
uvicorn apps.api:app --reload
```

- API: http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

- Frontend: http://localhost:5173

---

## 🤖 Example AI Queries

- "What activities do I have today?"
- "Summarize my schedule"
- "When is my next workout?"

---

## 🌐 API Endpoints

### Activities

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/activities` | List all activities |
| `POST` | `/activities` | Create a new activity |
| `PUT` | `/activities/{id}` | Update an activity |
| `DELETE` | `/activities/{id}` | Delete an activity |

### AI

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/ai/ask?q=your_question` | Ask a natural language question |
| `GET` | `/ai/summary` | Get an AI-generated summary |

---

## 🚀 Deployment

### Backend (Render)
1. Deploy FastAPI service
2. Add environment variables (API keys)

### Frontend (Vercel)
1. Connect GitHub repo
2. Set API base URL

---

## 🧪 Testing

```bash
pytest
```

Includes:
- API testing
- Core logic validation
- AI endpoint mocking

---

## 🧠 Future Improvements

- User authentication with database (signup/login)
- Chat history (ChatGPT-style)
- Activity analytics dashboard
- Improved UI/UX and animations
- Role-based access control

---

## 💼 Resume Description

Built a full-stack AI-powered web application using React and FastAPI, implementing CRUD operations and an LLM-based assistant for natural language interaction with user data.

---

## 👨‍💻 Author

**Cade Schiano**
- GitHub: [https://github.com/CadeSchiano](https://github.com/CadeSchiano)

---

## 📄 License

[MIT License](https://opensource.org/licenses/MIT)