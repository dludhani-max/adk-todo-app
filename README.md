# FastAPI Todo App with SQLite & Vanilla JS UI

A lightweight FastAPI todo application backed by SQLite with a responsive plain JavaScript frontend.

## Features

- **Full Todo CRUD Operations**: Create, list, retrieve, update, delete, and toggle todo items.
- **SQLite Database**: Persistent SQLite storage with configurable database path via the `DB_PATH` environment variable.
- **Vanilla JS Frontend**: Clean single-page application served directly from `/` with strikethrough styling for completed items.
- **Isolated Testing**: Comprehensive pytest suite using temporary SQLite databases for total test isolation.

## API Endpoints

- `GET /` — Serves the frontend web app (`static/index.html`).
- `GET /todos` — Returns all todo items.
- `POST /todos` — Creates a new todo item. Expects JSON `{ "title": "...", "description": "...", "completed": false }`.
- `GET /todos/{id}` — Returns a specific todo by ID (404 if not found).
- `PUT /todos/{id}` — Updates a todo by ID (404 if not found).
- `DELETE /todos/{id}` — Deletes a todo by ID (404 if not found).
- `PATCH /todos/{id}/toggle` — Flips the `completed` status of a todo by ID (404 if not found).

## Setup

1. **Clone the repository** (or navigate to project directory).
2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

Start the server using Uvicorn:

```bash
uvicorn app:app --reload --port 8001
```

Open your browser and navigate to `http://127.0.0.1:8001/` to use the app.

## Running the Tests

Run tests with `pytest`:

```bash
pytest
```
