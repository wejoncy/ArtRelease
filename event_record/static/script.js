document.addEventListener('DOMContentLoaded', () => {
    // Modal Elements
    const editModal = document.getElementById('edit-modal');
    const deleteModal = document.getElementById('delete-modal');
    const closeButtons = document.querySelectorAll('.close');
    const cancelDelete = document.getElementById('cancel-delete'); // Might be null

    // Form Elements
    const createEventForm = document.getElementById('create-event-form');
    const editForm = document.getElementById('edit-event-form');
    const deleteForm = document.getElementById('delete-event-form');

    // Event creation form listener
    if (createEventForm) {
        createEventForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const userData = document.getElementById('user').value;
            const messageInputValue = document.getElementById('message').value;
            const timeData = document.getElementById('time').value || new Date().toISOString().split('T')[0];
            let messageDataToSend;
            try {
                messageDataToSend = JSON.parse(messageInputValue);
            } catch (error) {
                messageDataToSend = messageInputValue;
            }
            try {
                const response = await fetch('/api/events/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user: userData, message: messageDataToSend, time: timeData })
                });
                if (response.ok) {
                    window.location.href = '/manage';
                } else {
                    alert('Failed to create event.');
                }
            } catch (error) {
                 alert('An error occurred.');
            }
        });
    }

    // Update event form listener
    if (editForm) {
        editForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const eventId = editForm.getAttribute('data-event-id');
            const userData = document.getElementById('edit-user').value;
            const messageInputValue = document.getElementById('edit-message').value;
            const timeData = document.getElementById('edit-time').value || new Date().toISOString().split('T')[0];
            let messageDataToSend;
             try {
                messageDataToSend = JSON.parse(messageInputValue);
            } catch (error) {
                messageDataToSend = messageInputValue;
            }
             try {
                const response = await fetch(`/api/events/${eventId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user: userData, message: messageDataToSend, time: timeData })
                });
                 if (response.ok) {
                    if (editModal) editModal.style.display = 'none';
                    window.location.href = '/manage';
                } else {
                     alert('Failed to update event.');
                }
            } catch (error) {
                 alert('An error occurred.');
            }
        });
    }

    // Delete event form listener
     if (deleteForm) {
        deleteForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const eventId = deleteForm.getAttribute('data-event-id');
            try {
                const response = await fetch(`/api/events/${eventId}`, { method: 'DELETE' });
                if (response.ok) {
                    if (deleteModal) deleteModal.style.display = 'none';
                    window.location.href = '/manage';
                } else {
                    const errorText = await response.text();
                    alert(`Failed to delete event: ${errorText}`);
                }
            } catch (error) {
                alert('An error occurred while deleting the event.');
            }
        });
    }

    // Close modals when clicking on close button
    if (closeButtons.length > 0) {
        closeButtons.forEach(button => {
            button.addEventListener('click', () => {
                if (editModal) editModal.style.display = 'none';
                if (deleteModal) deleteModal.style.display = 'none';
            });
        });
    }

    // Close modals when clicking outside
    window.addEventListener('click', (event) => {
        if (editModal && event.target === editModal) {
            editModal.style.display = 'none';
        }
        if (deleteModal && event.target === deleteModal) {
            deleteModal.style.display = 'none';
        }
    });

    // Cancel delete button listener
    if (cancelDelete) {
        cancelDelete.addEventListener('click', () => {
            if (deleteModal) deleteModal.style.display = 'none';
        });
    }

    // --- Show/Hide Past Events Logic ---
    const showPastToggle = document.getElementById('show-past-toggle');
    const eventListContainer = document.querySelector('.event-list'); // Use a more general selector if needed

    // Function to apply the filter based on checkbox state (remains the same)
    function applyPastEventFilter() {
        if (!eventListContainer) {
            // console.log("applyPastEventFilter: No event list container found."); // Debug
            return;
        }
        // Use window.todayDateStr if available, otherwise calculate
        const todayStr = window.todayDateStr || new Date().toISOString().split('T')[0];

        if (!showPastToggle) {
            // console.log("applyPastEventFilter: No toggle found, showing all."); // Debug
             // If no toggle exists, ensure nothing is hidden by this logic
             eventListContainer.querySelectorAll('.event.hidden-past').forEach(el => el.classList.remove('hidden-past'));
             return;
        }

        const showPast = showPastToggle.checked;
        // Select elements with 'event' class inside the container
        const events = eventListContainer.querySelectorAll('.event');
        // console.log(`applyPastEventFilter: Found ${events.length} events. Show past: ${showPast}`); // Debug

        if (events.length === 0) {
            // console.log("applyPastEventFilter: No event elements found to filter."); // Debug
            return;
        }

        events.forEach((eventElement) => { // Removed index as it wasn't used
            const eventTime = eventElement.getAttribute('data-time');

            if (!eventTime) {
                // console.log("applyPastEventFilter: Event element missing data-time, showing.", eventElement); // Debug
                eventElement.classList.remove('hidden-past'); // Ensure elements without time are shown
                return;
            }

            const isPast = eventTime < todayStr;
            // console.log(`applyPastEventFilter: Event time ${eventTime}, isPast: ${isPast}`); // Debug

            if (!showPast && isPast) {
                // Hide past events
                // console.log("applyPastEventFilter: Hiding past event.", eventElement); // Debug
                eventElement.classList.add('hidden-past');
            } else {
                // Show current/future events, or all events if showPast is true
                // console.log("applyPastEventFilter: Showing event.", eventElement); // Debug
                eventElement.classList.remove('hidden-past');
            }
        });
    }

    // Add listener to the toggle
    if (showPastToggle) {
        // Set initial checkbox state from localStorage (still useful for visual consistency)
        const savedPreference = localStorage.getItem('showPastEvents');
        if (savedPreference === 'true') {
            showPastToggle.checked = true;
        } else {
             showPastToggle.checked = false;
        }

        // Add the change listener which WILL call applyPastEventFilter on toggle
        showPastToggle.addEventListener('change', () => {
            localStorage.setItem('showPastEvents', showPastToggle.checked);
            applyPastEventFilter(); // Apply filter when checkbox changes
        });

    } else {
         // Fallback if no toggle exists (e.g., on a different page)
         const events = eventListContainer?.querySelectorAll('.event.hidden-past');
         events?.forEach(el => el.classList.remove('hidden-past'));
    }
});

// Edit event function
function editEvent(id) {
    const eventId = parseInt(id, 10);
    if (isNaN(eventId)) {
        alert("Error: Invalid event ID.");
        return;
    }

    const eventData = window.allEventsData ? window.allEventsData.find(event => event.id === eventId) : undefined;

    if (!eventData) {
        alert("Error: Could not retrieve event data.");
        return;
    }

    const user = eventData.user;
    const time = eventData.time;
    const messageData = eventData.message;

    const modal = document.getElementById('edit-modal');
    const form = document.getElementById('edit-event-form');
    const userInput = document.getElementById('edit-user');
    const messageInput = document.getElementById('edit-message');
    const timeInput = document.getElementById('edit-time');

    if (!messageInput) {
        return;
    }

    let displayMessage = '';

    if (messageData !== undefined && messageData !== null) {
        try {
            if (typeof messageData === 'object') {
                displayMessage = JSON.stringify(messageData, null, 2);
            } else {
                displayMessage = String(messageData);
            }
        } catch (e) {
            displayMessage = "Error displaying message data.";
        }
    }

    userInput.value = user || '';
    messageInput.value = displayMessage;
    timeInput.value = time || '';

    form.setAttribute('data-event-id', String(eventId));
    modal.style.display = 'block';
}

// Delete event function
function deleteEvent(id) {
    const modal = document.getElementById('delete-modal');
    const form = document.getElementById('delete-event-form');

    if (form && modal) { // Add checks
        form.setAttribute('data-event-id', id);
        modal.style.display = 'block';
    }
}
