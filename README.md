# FocusFlow: The Ultimate Student Dashboard

> A single, unified productivity app to organize your entire semester. Built with Vanilla JS and a FastAPI backend.

## 🌟 Inspiration

Every semester, students juggle deadlines, notes, grades, and resources across half a dozen apps and platforms. I wanted a single unified tool that would not only organize this chaos but also actively motivate—integrating analytics and streak-based achievements into the everyday workflow.

## 🚀 What it does

FocusFlow is a unified productivity dashboard for students. It delivers all key features in a single, fast-loading page:

* **Task Management:** Organize tasks in three distinct layouts: a drag-and-drop **Kanban Board**, a full-page **Calendar**, or a dense, sortable **List View**.
* **Study Analytics:** Track your Pomodoro sessions with a custom-built bar chart. A **Study Streak** tracker and **Achievement** system motivate you to stay consistent.
* **Flashcard Decks:** Create and study your own flashcard decks, complete with an answer-checking study mode.
* **Grade Tracker:** A simple, powerful calculator to track assignments and weighted grades by course.
* **Persistent Music Player:** Upload your favorite study music, which persists between sessions, and control playback while you work.
* **Calm UI:** A beautiful, responsive interface with full **Light and Dark Mode** support.

All data is **instantly persistent**, saving every change directly to a dedicated backend.

## 🛠️ Tech Stack

* **Frontend:** Vanilla JavaScript (ES6+), Tailwind CSS, HTML5
* **Backend:** FastAPI (Python), Uvicorn
* **Persistence:**
    * **App Data (JSON):** All user data (tasks, grades, etc.) is serialized and saved to a `data/app_data.json` file on the server.
    * **Music Files:** Uploaded audio files are stored in a `/music/` directory on the server.
* **Tooling:** `uv` (for Python package management and running)

## 🏃 Getting Started

This guide will get you a local copy up and running.

### Prerequisites

You must have [Python 3.10+](https://www.python.org/downloads/) and [uv](https://github.com/astral-sh/uv) installed.

You can install `uv` with:
```bash
# macOS / Linux
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
# Windows
powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```

### Clone the Repository

```bash
git clone [https://github.com/FilbertNg/FocusFlow.git](https://github.com/FilbertNg/FocusFlow.git)
cd FocusFlow
```

### Installation

```bash
uv sync
```

### Running the App

```bash
uv run main.py
```

### Accessing the App

Open your browser and navigate to `http://localhost:8000`.
