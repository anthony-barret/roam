from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.trips.models import Trip


class TripModelTests(TestCase):
    def test_rating_zero_is_valid(self):
        """
        Rating can be zero.
        """
        trip = Trip(
            name='Trip to test_rating_zero_is_valid',
            destination='Testland',
            description='Trip to Testland',
            rating=0,
        )
        trip.full_clean()

    def test_rating_ten_is_valid(self):
        """
        Rating can be ten.
        """
        trip = Trip(
            name='Trip to test_rating_ten_is_valid',
            destination='Testland',
            description='Trip to Testland',
            rating=10,
        )
        trip.full_clean()

    def test_rating_negative_number_is_invalid(self):
        """
        Rating cannot be negative.
        """
        trip = Trip(
            name='Trip to test_rating_negative_number_is_invalid',
            destination='Testland',
            description='Trip to Testland',
            rating=-1,
        )
        with self.assertRaises(ValidationError):
            trip.full_clean()

    def test_rating_above_ten_is_invalid(self):
        """
        Rating cannot be greater than ten.
        """
        trip = Trip(
            name='Trip to test_rating_above_ten_is_invalid',
            destination='Testland',
            description='Trip to Testland',
            rating=11,
        )
        with self.assertRaises(ValidationError):
            trip.full_clean()

    def test_trip_name_is_required(self):
        trip = Trip(
            destination='Testland',
            description='Trip to Testland',
            rating=5,
        )
        with self.assertRaises(ValidationError):
            trip.full_clean()

    def test_trip_destination_is_required(self):
        trip = Trip(
            name='Trip to test_trip_destination_is_required',
            description='Trip to Testland',
            rating=5,
        )
        with self.assertRaises(ValidationError):
            trip.full_clean()
