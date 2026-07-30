from django.test import TestCase, Client
from django.urls import reverse
import json
from .models import ScannedTag

class LandingPageTest(TestCase):
    def test_landing_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_landing_page_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'rfid/landing.html')

class ScannerIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_receive_scan(self):
        payload = [
            {
                "data": "E280119120007204791E0AD1",
                "antenna": 1,
                "rssi": -60
            },
            {
                "data": "E280119120007204791E0AD2",
                "antenna": 2,
                "rssi": -65
            }
        ]
        response = self.client.post(
            reverse('receive_scan'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ScannedTag.objects.count(), 2)

    def test_get_scans(self):
        ScannedTag.objects.create(epc="TEST-TAG-1")
        response = self.client.get(reverse('get_scans'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['scans']), 1)
        self.assertEqual(data['scans'][0]['epc'], "TEST-TAG-1")

    def test_clear_scans(self):
        ScannedTag.objects.create(epc="TEST-TAG-1")
        response = self.client.get(reverse('clear_scans'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ScannedTag.objects.count(), 0)
