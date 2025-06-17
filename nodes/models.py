from django.db import models
import uuid

class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.GenericIPAddressField()
    location = models.CharField(max_length=100)  # E.g., 'PB', 'SP', 'MG'
    status = models.CharField(max_length=10, choices=[('online', 'Online'), ('offline', 'Offline')], default='offline')
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.location} ({self.ip}) - {self.status}'
