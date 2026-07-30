import json
import logging
import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ScannedTag

logger = logging.getLogger(__name__)

def landing_page(request):
    """
    Renders the RFID scanner landing page.
    """
    return render(request, 'rfid/landing.html')

@csrf_exempt
def receive_scan(request):
    """
    Endpoint for Zebra FX9600 IoT Connector to POST scanned tags.
    """
    if request.method == 'POST':
        try:
            # Enhanced logging for debugging Zebra reader
            remote_addr = request.META.get('REMOTE_ADDR')
            headers = {k: v for k, v in request.META.items() if k.startswith('HTTP_')}
            raw_body = request.body.decode('utf-8')
            
            # Write to a dedicated log file for the user to monitor
            from datetime import datetime
            log_path = r'C:\Users\Jesús Ibarra\PycharmProjects\Scanner-Zebra-RFID\zebra_traffic.log'
            with open(log_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"\n--- INCOMING REQUEST AT {datetime.now().isoformat()} FROM {remote_addr} ---\n")
                log_file.write(f"Headers: {json.dumps(headers, indent=2)}\n")
                log_file.write(f"Body: {raw_body}\n")
                log_file.write(f"-------------------------------------------\n")
                log_file.flush()
                os.fsync(log_file.fileno()) # Force write to disk
            
            # Also print to console
            print(f"\n--- INCOMING REQUEST FROM {remote_addr} ---")
            print(f"Body: {raw_body[:100]}...") # Short version for console
            
            data = json.loads(raw_body)
            tags_to_create = []

            # Normalize data to a list of items
            items = []
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                # Some Zebra configurations wrap data in 'tagData' or similar
                items = data.get('tagData') or data.get('tags') or [data]
            
            if isinstance(items, list):
                for item in items:
                    # Skip heartbeats
                    if item.get('isHeartBeat') is True:
                        continue
                        
                    # Try different keys for the EPC/Data
                    epc = item.get('data') or item.get('idHex') or item.get('epc') or item.get('tagID')
                    if epc:
                        tags_to_create.append(ScannedTag(
                            epc=epc,
                            reader_ip=request.META.get('REMOTE_ADDR'),
                            antenna=item.get('antenna') or item.get('antennaID'),
                            rssi=item.get('peakRssi') or item.get('rssi')
                        ))
                
                if tags_to_create:
                    ScannedTag.objects.bulk_create(tags_to_create)
                
                return JsonResponse({'status': 'success', 'count': len(tags_to_create)})
            
            return JsonResponse({'status': 'error', 'message': 'Invalid data format'}, status=400)
        except Exception as e:
            logger.error(f"DEBUG ERROR: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

def get_scans(request):
    """
    Returns the latest scanned tags in JSON format for the frontend.
    """
    # Get scans from the last 10 minutes, or just the last 50 scans
    scans = ScannedTag.objects.all()[:50]
    data = [
        {
            'epc': scan.epc,
            'timestamp': scan.timestamp.isoformat(),
            'antenna': scan.antenna,
            'rssi': scan.rssi
        } for scan in scans
    ]
    return JsonResponse({'scans': data})

def clear_scans(request):
    """
    Clears the scanned tags database.
    """
    ScannedTag.objects.all().delete()
    return JsonResponse({'status': 'success'})
