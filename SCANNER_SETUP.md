### Zebra FX7500/FX9600 Configuration Guide

This guide outlines the steps to connect a Zebra FX-series RFID reader to the Django interface using the IoT Connector.

#### 1. Access the Web Interface
- Open your browser and navigate to the reader's IP (e.g., `http://192.168.1.249`).
- Log in with your credentials (default: `admin` / `change`).

#### 2. Configure the IoT Connector
1. **Navigate to Communication > IoT Connector**.
2. **Endpoints Tab**:
   - Add a new endpoint named `DjangoAPI`.
   - **Type**: `HTTP POST`.
   - **URL**: `http://<YOUR_PC_IP>:8000/api/receive-scan/`.
   - **Authentication**: `NONE`.
   - Verify status shows `Connected` or code `200` after saving.
3. **Interface Mapping Tab**:
   - Find the **Tag Data** row.
   - Set the **Endpoint** to `DjangoAPI`.
   - Click **Apply**.
4. **Configuration Tab**:
   - Ensure **IoT Connector Status** is `Started`.

#### 3. Enable Inventory Transmission
- Navigate to **Inventory > Settings**.
- Set **Primary Mode** to `IoT Connector`.
- Click **Apply**.

#### 4. Run the Inventory
- Go to **Inventory > Control**.
- Click **Start**. Tags will now be pushed to the Django backend.

#### 5. Troubleshooting
- **Connectivity**: Use `System > Utilities > Ping` to verify the reader can reach your PC's IP.
- **Logs**: Check `System > Logs` for HTTP error codes (404, 500, etc.).
- **Firewall**: Ensure port 8000 is open on your PC.
- **Reboot**: A reader reboot (`System > Reboot/Reset`) is often required after changing the Primary Mode.
