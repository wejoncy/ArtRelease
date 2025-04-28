#!/bin/bash

# Base URL for the API (adjust if necessary)
BASE_URL="http://127.0.0.1:8000"
# Get today's date in YYYY-MM-DD format
TODAY=$(date +%Y-%m-%d)

# --- POST a new event ---
# Note: The 'message' field can be complex JSON. Adjust the payload accordingly.
# Assuming ID is assigned by the server now.
echo "Adding a new event..."
curl -X POST "${BASE_URL}/api/events/" \
     -H "Content-Type: application/json" \
     -d '{
           "user": "user1",
           "message": "First event message",
           "time": "'"${TODAY}"'"
         }'
echo -e "\n"
echo "Script finished creating events."
