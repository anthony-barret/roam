from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

class TripStatus(models.TextChoices):
    PLANNED = 'planned'
    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name

    @property
    def flag(self):
        return ''.join(
            chr(ord(char) + 127397)
            for char in self.code.upper()
        )


class Trip(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name='trips',
    )
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError({
                'end_date': 'The end date cannot be before the start date.'
            })

    @property
    def full_stars(self):
        return range(self.rating // 2)

    @property
    def half_star(self):
        return self.rating % 2 == 1

    @property
    def empty_stars(self):
        return range(5 - self.rating // 2 - int(self.half_star))


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'name',
            'city',
            'country',
            'start_date',
            'end_date',
            'description',
            'status',
            'rating',
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'country': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'start_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'end_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'rating': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0,
                    'max': 10,
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].label_from_instance = (
            lambda country: f'{country.flag} {country.name}'
        )
