# Smart Activity Tracker

## Overview
Smart Activity Tracker is a Python-based application that allows users to manage and display activities in a structured and readable format. Each activity includes details such as title, category, location, and time.

This project is designed with clean separation of concerns and scalability in mind, making it easy to expand with features like user input, data persistence, filtering, or a web/API interface in the future.

---

##  Tech Stack
- **Python 3.11**
- Virtual Environments (`venv`)
- Python Standard Library (no external dependencies yet)

---

## Project Structure
smart_activity_tracker/
│
├── apps/
│ ├── init.py
│ ├── core.py # Core logic and activity handling
│ └── main.py # Application entry point
│
├── requirements.txt
├── README.md
└── .gitignore


---

## How to Run the Project

1. Clone the repository:

git clone https://github.com/CadeSchiano/smart_activity_tracker.git
cd smart_activity_tracker

python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

python3 apps/main.py

---

## Current Features

Defines activities with structured data

Displays activity details in a clean, readable format

Modular code structure separating core logic and execution

---

## Future Improvements

User input for creating activities

Data persistence (file or database storage)

Filtering and searching activities

REST API using FastAPI

Web or mobile frontend integration

---

## Author

Cade Schiano
Computer Science Student
GitHub: https://github.com/CadeSchiano
---
