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
