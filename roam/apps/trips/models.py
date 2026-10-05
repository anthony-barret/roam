from django.db import models


# Create your models here.

class TripStatus(models.TextChoices):
    PLANNED = 'planned'
    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


