from django.db import models

class ScannedTag(models.Model):
    epc = models.CharField(max_length=255, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    reader_ip = models.GenericIPAddressField(null=True, blank=True)
    antenna = models.IntegerField(null=True, blank=True)
    rssi = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.epc} @ {self.timestamp}"
