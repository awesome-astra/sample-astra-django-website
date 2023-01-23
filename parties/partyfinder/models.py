import uuid

from django.db import models
from django.utils import timezone

# A model for this app
class Party(models.Model):
  id = models.UUIDField(
    primary_key = True,
    default = uuid.uuid4,
    editable = False,
  )
  city = models.CharField(max_length=50)
  name = models.CharField(max_length=200)
  date = models.DateTimeField(default=timezone.now)
