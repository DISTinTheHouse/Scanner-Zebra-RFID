### Zebra RFID Scanner Interface (Django)

A high-performance web interface designed for Zebra FX7500/FX9600 fixed RFID readers. This application provides real-time tag monitoring via a mobile-optimized dashboard, leveraging the Zebra IoT Connector for hardware-to-backend communication.

#### Key Features
- **Real-Time Monitoring**: Live EPC tag list with antenna and RSSI metadata.
- **Hardware Integration**: Optimized for Zebra's HTTP POST push mechanism (IoT Connector).
- **Mobile-First Design**: Built with Tailwind CSS for warehouse handhelds and Zebra scanners.
- **Diagnostic Tools**: Built-in logging and testing suite for network verification.

---

#### Quick Start

##### 1. Prerequisites
- Python 3.10+
- Access to a Zebra FX series reader (or use the simulation tools).

##### 2. Installation
```powershell
# Clone the repository
git clone <repository-url>
cd Scanner-Zebra-RFID

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate
```

##### 3. Start the Server
```powershell
python manage.py runserver 0.0.0.0:8000
```
*Note: Binding to `0.0.0.0` is required so the scanner can reach your computer.*

---

#### Hardware Configuration

To connect a Zebra FX reader (Firmware 3.x+):

1. **IoT Connector**:
   - Go to `Communication > IoT Connector > Endpoints`.
   - Add a new **HTTP POST** endpoint pointing to: `http://<YOUR_PC_IP>:8000/api/receive-scan/`.
2. **Interface Mapping**:
   - Map **Tag Data** to your new endpoint.
3. **Primary Mode**:
   - In `Inventory > Settings`, set **Primary Mode** to **IoT Connector**.
4. **Start**:
   - Click **Start** in the `Inventory > Control` menu.

Detailed setup instructions are available in [SCANNER_SETUP.md](./SCANNER_SETUP.md).

---

#### Diagnostics & Testing

- **Live Logs**: Monitor real scanner traffic in real-time:
  ```powershell
  Get-Content -Path "zebra_traffic.log" -Wait
  ```
- **Simulate Tags**: Test the backend without hardware:
  ```powershell
  curl.exe -X POST http://localhost:8000/api/receive-scan/ -H "Content-Type: application/json" -d '[{"data": "TEST-EPC-12345", "antenna": 1, "peakRssi": -60}]'
  ```

For more diagnostic commands, see [commands.md](./commands.md).

---

#### Project Structure
- `/RFID`: Django app handling ingestion and storage.
- `/templates`: Responsive Tailwind UI.
- `zebra_traffic.log`: Forensic log for incoming scanner payloads.
- `commands.md`: Advanced PowerShell tools for network debugging.
