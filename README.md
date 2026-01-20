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

# Smart Activity Tracker

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#license)

Smart Activity Tracker is a small, modular Python application for defining, organizing, and displaying user activities (title, category, location, and time). The codebase emphasizes clarity and separation of concerns so it can be extended with persistence, filtering, or a web/API layer.

## Table of Contents
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Layout](#project-layout)
- [Quickstart](#quickstart)
- [Usage](#usage)
- [Development](#development)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)
- [Author / Contact](#author--contact)

## Key Features
- Define activities with structured data (title, category, location, time)
- Clean, human-readable display of activity details
- Modular design: core logic separated from the application entry point

## Tech Stack
- Python 3.11
- Standard library (no runtime external dependencies by default)
- Virtual environments for development (`venv`)

## Project Layout
```
smart_activity_tracker/
├── apps/
│   ├── __init__.py
│   ├── core.py        # Core logic and activity handling
│   └── main.py        # Application entry point
├── requirements.txt
├── README.md
└── .gitignore
```

## Quickstart
Recommended: use a virtual environment to keep dependencies isolated.

1. Clone the repository and enter the directory

```bash
git clone https://github.com/CadeSchiano/smart_activity_tracker.git
cd smart_activity_tracker
```

2. Create and activate a virtual environment (macOS/Linux - zsh)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies (if any)

```bash
pip install -r requirements.txt
```

4. Run the app

You can run the package module or the script directly:

```bash
python -m apps.main
# or
python3 apps/main.py
```

## Usage
The application currently prints activity information to the console (see `apps/core.py` for the data model and formatting helpers). Extend `apps/main.py` to add input handling, file/database storage, or an API layer.

## Development
- Branch from `main` for feature work.
- Keep changes small and focused; open a PR for review.

Recommended developer workflow (example):

```bash
# create a feature branch
git checkout -b feat/add-persistence

# run the app locally during development
python -m apps.main
```

If you add third-party packages, update `requirements.txt` with pinned versions, e.g. `fastapi==0.95.0`.


## Roadmap
- Add user-driven activity creation and editing
- Add simple file-based persistence (JSON/CSV)
- Add filtering/searching capabilities
- Add optional REST API (FastAPI) and a small web UI

## License
This project does not include a license file yet. If you'd like to make the project open source, consider adding an `LICENSE` (for example, the MIT License).

## Author / Contact
Cade Schiano — Software Engineering Student
- GitHub: https://github.com/CadeSchiano

