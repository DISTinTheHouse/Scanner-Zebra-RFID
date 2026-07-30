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
- Access to a Zebra FX series reader.
- <img width="921" height="527" alt="zebra-reader-example" src="https://github.com/user-attachments/assets/0cc50048-cd36-4bca-b4e8-fcbd9173b87e" />


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

- <img width="1324" height="824" alt="zebra-config-example" src="https://github.com/user-attachments/assets/56e0819e-f5f9-469f-921a-942301c62a35" />

Save the changes:
<img width="1060" height="765" alt="image" src="https://github.com/user-attachments/assets/4d895505-c343-4721-9928-904720e4d5aa" />

Go to "Connections" and there you go:
<img width="1067" height="450" alt="image" src="https://github.com/user-attachments/assets/80bced88-c0b2-4afd-8eba-5e0ec36762e9" />


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
