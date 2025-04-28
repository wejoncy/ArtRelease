# Base URL for the API (adjust if necessary)
$baseUrl = "http://127.0.0.1:8000"

# --- POST a new event ---
Write-Host "Adding a new event..."
$newEvent1 = @{
    user = "user1"
    message = "First event message"
    time = (Get-Date -Format 'yyyy-MM-dd') # Use today's date
} | ConvertTo-Json

try {
    Invoke-RestMethod -Method Post -Uri "$baseUrl/api/events/" -ContentType 'application/json' -Body $newEvent1
} catch {
    Write-Error "Failed to add event 1: $($_.Exception.Message)"
}
Write-Host "`n"

Write-Host "Script finished creating events."
