from datetime import date

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

class TripStatus(models.TextChoices):
    PLANNED = 'planned'
    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class Trip(models.Model):
    name = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=TripStatus.choices,
        default=TripStatus.PLANNED,
    )
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'name',
            'destination',
            'start_date',
            'end_date',
            'description',
            'status',
            'rating',
        ]
        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'date'},
            ),
            'end_date': forms.DateInput(
                attrs={'type': 'date'},
            ),
            'description': forms.Textarea(
                attrs={'rows': 5},
            ),
        }
