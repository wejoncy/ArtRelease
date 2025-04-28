# Event Manager

A FastAPI application for managing events with a beautiful UI.

## Features

- Create, read, update, and delete events via JSON API
- Events stored with timestamp-based IDs and date
- Event messages can be any JSON-serializable object
- Today's events highlighted
- Separate pages for viewing event feed and managing events
- Responsive UI with modal dialogs for actions

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
# Use app:app since the file is now app.py
uvicorn app:app --reload
```

4. Open your browser and navigate to http://localhost:8000 (Event Feed) or http://localhost:8000/manage (Event Manager)

## Project Structure

- `app.py` - FastAPI application and routes (formerly main.py)
- `database.py` - Event storage and data management
- `templates/`
    - `index.html` - Event feed display (formerly home.html)
    - `manage.html` - Event management UI (formerly index.html)
- `static/` - CSS and JavaScript files
- `events.json` - Persistent storage file for events
- `requirements.txt` - Python dependencies