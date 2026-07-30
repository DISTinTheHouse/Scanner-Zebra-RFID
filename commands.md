### RFID Scanner Diagnostic & Test Suite

This document provides essential commands for monitoring scanner traffic, verifying network connectivity, and simulating tag data.

---

#### 1. Real-Time Traffic Monitor
Follow the dedicated forensic log to see raw payloads and headers from the Zebra reader.

**Command (PowerShell):**
```powershell
Get-Content -Path "zebra_traffic.log" -Wait
```

---

#### 2. Network Connectivity Verification
Verify if the reader (e.g., `192.168.1.249`) is attempting to communicate with your computer on the Django port.

**Command (PowerShell):**
```powershell
# Check for active TCP connections from the reader's IP
Get-NetTCPConnection -RemoteAddress 192.168.1.249 -ErrorAction SilentlyContinue | Select-Object RemoteAddress, LocalPort, State
```

---

#### 3. Firewall Validation
Confirm that the inbound rule for the RFID scanner is active and correctly configured.

**Command (PowerShell):**
```powershell
Get-NetFirewallRule -DisplayName "Django RFID Scanner" | Select-Object Name, Enabled, Direction, Action
```

---

#### 4. Data Simulation (Server Health Check)
Send a simulated tag to verify the backend ingestion pipeline is functional.

**Command (PowerShell):**
```powershell
curl.exe -X POST http://localhost:8000/api/receive-scan/ `
  -H "Content-Type: application/json" `
  -d '[{"data": "SIMULATED-EPC-999", "antenna": 1, "peakRssi": -50}]'
```

---

#### 5. Database Management
Clear all current scans to prepare for a fresh inventory session.

**Command (PowerShell):**
```powershell
curl.exe http://localhost:8000/api/clear-scans/
```
