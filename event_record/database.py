from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime
import json
import os

# Data model
class Event(BaseModel):
    id: int
    user: str
    message: Any
    time: str # This will now store YYYY-MM-DD

# In-memory database
events: Dict[int, Event] = {}
DATA_FILE = "events.json"

# Load data from file if exists
def load_data():
    global events
    if os.path.exists(DATA_FILE):
        try:
            # Specify UTF-8 encoding for reading
            with open(DATA_FILE, "r", encoding='utf-8') as f:
                data = json.load(f)
                # Ensure data loaded is correctly parsed into Event models
                events = {}
                for k, v in data.items():
                    try:
                        events[int(k)] = Event(**v)
                    except Exception as parse_error:
                        print(f"Error parsing event {k}: {parse_error}. Skipping.")

        except json.JSONDecodeError as e:
             print(f"Error decoding JSON from {DATA_FILE}: {e}")
             # Decide how to handle corrupted file: backup and start fresh?
             # For now, just print error and start with empty events
             events = {}
        except Exception as e:
            print(f"Error loading data from {DATA_FILE}: {e}")
            events = {} # Fallback to empty dict on other errors

# Save data to file
def save_data():
    """Saves the current events dictionary to the JSON file."""
    try:
        # Specify UTF-8 encoding for writing
        with open(DATA_FILE, "w", encoding='utf-8') as f:
            # Convert event objects to dictionaries using Pydantic's .dict() method
            # This ensures complex types within 'message' are properly handled by Pydantic first
            json_data = {str(k): v.dict() for k, v in events.items()}

            # Dump the dictionary to JSON, explicitly setting ensure_ascii=False
            json.dump(
                json_data,
                f,
                indent=2,
                ensure_ascii=False # This is the crucial flag
            )
    except Exception as e:
        print(f"Error saving data to {DATA_FILE}: {e}")


# CRUD operations
def get_events() -> List[Event]:
    """Loads data from file and returns a sorted list of events."""
    load_data() # Reload data from file every time events are requested
    # Sort by date string (YYYY-MM-DD) descending to show newest first
    return sorted(events.values(), key=lambda x: x.time, reverse=True)

def get_event_by_id(event_id: int) -> Optional[Event]:
    """Gets a single event by its ID from the in-memory dictionary."""
    # No need to reload here if get_events already does,
    # but might be safer depending on usage patterns.
    # Consider if load_data() should be called here too.
    # For now, assume 'events' is reasonably up-to-date.
    return events.get(event_id)

def add_event(event: Event) -> Event:
    events[event.id] = event
    save_data()
    return event

def update_event(event_id: int, event_data: Event) -> bool:
    if event_id in events:
        # Ensure the ID from the path parameter is used, not potentially from event_data
        event_data.id = event_id
        events[event_id] = event_data
        save_data()
        return True
    return False

def delete_event(event_id: int) -> bool:
    if event_id in events:
        del events[event_id]
        save_data()
        return True
    return False

# Remove initial load_data call from here if it exists,
# it will now be called within get_events or explicitly in main.py startup.
# load_data()
