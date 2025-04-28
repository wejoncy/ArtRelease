from fastapi import FastAPI, Request, HTTPException # Removed Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime
import time
import json
import os
# Import the new function and potentially the 'events' dict if needed elsewhere (though prefer functions)
from database import get_events, add_event, update_event, delete_event, Event, get_event_by_id

# Define an EventCreate model for handling JSON requests
class EventCreate(BaseModel):
    user: str
    message: Any
    time: Optional[str] = None  # Accepts YYYY-MM-DD string

app = FastAPI(
    title="ArtRelease Event Manager",
    description="API for creating, viewing, updating, and deleting art release events. Provides both HTML views and a JSON API.",
    version="0.1.0" # Add version
)

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
# Mount static files directory
app.mount("/static", StaticFiles(directory=CUR_DIR+"/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory=CUR_DIR+"/templates")

def format_message_for_display(message: Any) -> str:
    """Formats message for HTML display, handling complex types."""
    if isinstance(message, str):
        # Return simple strings directly
        return message
    else:
        try:
            # Convert non-strings to indented JSON string with Unicode preserved
            return json.dumps(message, indent=2, ensure_ascii=False)
        except Exception:
            # Fallback if json.dumps fails
            return str(message)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main HTML page structure."""
    # Remove event fetching and processing from here
    # The 'today' variable is also removed as it's not needed for server-side rendering anymore
    return templates.TemplateResponse("index.html", {
        "request": request,
        # Remove "events" and "today" from the context passed to the template
    })

@app.get("/manage", response_class=HTMLResponse)
async def manage_events(request: Request): # Removed show_past parameter
    """Serve the event management page."""
    # Keep this as is for now, as it might use server-side rendering differently
    # or pass the JSON string for its own JS logic.
    # If manage.html should also load dynamically, it needs similar changes.
    events_raw = get_events()
    today_str = datetime.now().strftime("%Y-%m-%d")

    events_filtered = events_raw # No filtering

    events_for_template = []
    for event in events_filtered:
        event_dict = event.dict()
        event_dict['display_message'] = format_message_for_display(event.message)
        events_for_template.append(event_dict)

    events_json_string = json.dumps(events_for_template, ensure_ascii=False)

    return templates.TemplateResponse("manage.html", {
        "request": request,
        "events": events_for_template,
        "today": today_str,
        "events_json": events_json_string,
    })

# --- API Endpoints ---

# Add a new GET endpoint to fetch all events as JSON, including formatted messages
@app.get("/api/events/", response_model=List[dict]) # Return list of dicts
async def get_events_json():
    """Retrieve all events formatted for API consumption."""
    events_raw = get_events()
    events_for_api = []
    for event in events_raw:
        event_dict = event.dict()
        # Add the formatted message directly for the client
        event_dict['display_message'] = format_message_for_display(event.message)
        events_for_api.append(event_dict)
    return events_for_api


@app.post("/api/events/", response_model=Event)
async def create_event_json(event_data: EventCreate):
    """Handle JSON-based event creation for API clients."""
    current_date = datetime.now().date()
    # Use milliseconds timestamp for a more unique ID
    timestamp = int(time.time() * 1000)

    # Use provided date string if available and valid, otherwise use current date
    event_date_str = event_data.time
    if event_date_str:
        try:
            parsed_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()
            event_date = parsed_date.isoformat()
        except ValueError:
            event_date = current_date.isoformat() # Default to current date on invalid format
    else:
        event_date = current_date.isoformat() # Default to current date if not provided

    # Create the Event object
    event = Event(
        id=timestamp,
        user=event_data.user,
        message=event_data.message,
        time=event_date
    )
    # Add event to database (which handles saving)
    added_event = add_event(event)
    return added_event


@app.put("/api/events/{event_id}", response_model=Event)
async def update_event_json(event_id: int, event_data: EventCreate):
    """Handle JSON-based event update for API clients."""
    current_date = datetime.now().date()

    # Check if event exists using the new database function
    existing_event = get_event_by_id(event_id)
    if not existing_event:
         raise HTTPException(status_code=404, detail="Event not found")

    # Use provided date string if available and valid, otherwise use existing date
    event_date_str = event_data.time
    if event_date_str:
        try:
            parsed_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()
            event_date = parsed_date.isoformat()
        except ValueError:
            # If format is invalid, keep the existing date instead of defaulting to today
            event_date = existing_event.time
    else:
        # If date is not provided in update, keep the original date
        event_date = existing_event.time

    # Create the updated Event object
    updated_event_data = Event(
        id=event_id, # Ensure the ID remains the same
        user=event_data.user,
        message=event_data.message,
        time=event_date
    )

    # Update event in database (which handles saving)
    success = update_event(event_id, updated_event_data)
    if not success:
        # This case should be rare if the initial check passed, but handle defensively
        raise HTTPException(status_code=404, detail="Event not found during update")

    # Return the updated event data
    # Fetching again ensures consistency after update_event saves.
    refreshed_event = get_event_by_id(event_id) # Use the function again
    if not refreshed_event:
         raise HTTPException(status_code=500, detail="Failed to retrieve event after update") # Should not happen
    return refreshed_event


@app.delete("/api/events/{event_id}", response_model=dict)
async def delete_event_json(event_id: int):
    """Handle JSON-based event deletion for API clients."""
    # Attempt to delete the event using the database function
    success = delete_event(event_id)

    # Check if the deletion was successful (i.e., the event ID was found)
    if not success:
        # If delete_event returned False, the ID was not found
        raise HTTPException(status_code=404, detail="Event not found")

    # If deletion was successful, return a success message
    return {"success": True, "message": "Event deleted successfully"}

# --- Main execution ---
if __name__ == "__main__":
    import uvicorn
    # Update the app reference to 'app:app' because the file is now app.py
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) # Added reload=True for convenience
