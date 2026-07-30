# Requirements

### Overview & Goals
Scale the RFID application to integrate with a real Zebra FX9600-4 fixed reader at IP 192.168.1.252. The system will use the scanner's IoT Connector to push data via HTTP POST and the frontend will display these scans using short polling.

### Scope
- **In Scope**:
    - Django model to persist scanned RFID tags.
    - REST endpoint to receive JSON data from the FX9600.
    - REST endpoint to serve recent scans to the frontend.
    - Updated Tailwind UI to fetch real data from the backend.
- **Out of Scope**:
    - Automated configuration of the FX9600 (manual setup required).
    - WebSocket implementation (deferred for simplicity).
    - Advanced inventory management (basic listing only).

# Technical Design

### Key Decisions
- **Persistence**: Use a simple Django model `ScannedTag` with fields for EPC, timestamp, and reader info.
- **Integration**: The FX9600 "HTTP POST" transport will be used. The endpoint must be CSRF-exempt if the scanner doesn't support CSRF tokens (standard for IoT devices).
- **Polling**: Frontend will poll every 2 seconds to refresh the tag list.

### File Structure
- `RFID/models.py`: Added `ScannedTag` model.
- `RFID/views.py`: Added `receive_scan` (POST) and `get_scans` (GET) views.
- `RFID/urls.py`: Updated with new API paths.
- `templates/rfid/landing.html`: Updated JS logic for polling.

# Delivery Steps

### ✓ Step 1: Implement ScannedTag Model
Define the data structure for storing scans.

- Create `ScannedTag` model in `RFID/models.py`.
- Run migrations to update the database.

### ✓ Step 2: Create API Endpoints for Scanner Integration
Implement the backend logic to receive and serve tag data.

- Implement `receive_scan` view (CSRF exempt) to process JSON from FX9600.
- Implement `get_scans` view to return tags as JSON.
- Register endpoints in `RFID/urls.py`.

### ✓ Step 3: Update Frontend for Real-time Polling
Connect the UI to the backend API.

- Replace mock scanning logic in `landing.html` with AJAX polling.
- Update UI status indicators based on backend connectivity.
- Add a "Scanner IP" indicator in the UI.

### ✓ Step 4: Verification and Configuration Guide
The application is verified with mock data and the configuration guide is updated for the FX9600.

- Test endpoints with `curl` (Verified by user).
- Update `SCANNER_SETUP.md` with correct scanner IP and detailed IoT Connector path.
- Update UI to reflect the correct scanner IP.
