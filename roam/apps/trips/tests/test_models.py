from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.trips.models import Country, Trip


class TripModelTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            name='Testland',
            code='TL',
        )

    def test_rating_zero_is_valid(self):
        """
        Rating can be zero.
        """
        trip = Trip(
            name='Trip to test_rating_zero_is_valid',
            city='Test',
            country=self.country,
            description='Trip to the city of tests',
            rating=0,
        )
        trip.full_clean()

    def test_rating_ten_is_valid(self):
        """
        Rating can be ten.
        """
        trip = Trip(
            name='Trip to test_rating_ten_is_valid',
            city='Test',
            country=self.country,
            description='Trip to the city of tests',
            rating=10,
        )
        trip.full_clean()

    def test_rating_negative_number_is_invalid(self):
        """
        Rating cannot be negative.
        """
        trip = Trip(
            name='Trip to test_rating_negative_number_is_invalid',
            city='Test',
            country=self.country,
            description='Trip to the city of tests',
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
            city='Test',
            country=self.country,
            description='Trip to the city of tests',
            rating=11,
        )
        with self.assertRaises(ValidationError):
            trip.full_clean()

    def test_trip_name_is_required(self):
        """
        Trip name must be provided.
        """
        trip = Trip(
            city='Test',
            country=self.country,
            description='Trip to the city of tests',
            rating=5,
        )
        with self.assertRaises(ValidationError):
            trip.full_clean()

    def test_trip_city_is_required(self):
        """
        Trip city must be provided.
        """
        trip = Trip(
            name='Trip to test_trip_city_is_required',
            country=self.country,
            description='Trip to the city of tests',
            rating=5,
        )
        with self.assertRaises(ValidationError):
            trip.full_clean()

    def test_trip_country_is_required(self):
        """
        Trip country must be provided.
        """
        trip = Trip(
            name='Trip to test_trip_country_is_required',
            city='Test',
            description='Trip to the city of tests',
            rating=5,
        )
        with self.assertRaises(ValidationError):
            trip.full_clean()

    def test_trip_description_is_required(self):
        """
        Trip description must be provided.
        """
        trip = Trip(
            name='Trip to test_trip_description_is_required',
            city='Test',
            country=self.country,
            rating=5,
        )
        with self.assertRaises(ValidationError):
            trip.full_clean()

    def test_trip_start_date_must_be_before_end_date(self):
        """
        Trip start date must be before end date.
        """
        trip = Trip(
            name='Trip to test_trip_start_date_must_be_before_end_date',
            city='Test',
            country=self.country,
            description='Trip to the city of tests',
            start_date=date(2026, 10, 11),
            end_date=date(2026, 10, 9),
            rating=5,
        )
        with self.assertRaises(ValidationError):
            trip.full_clean()

    def test_updated_at_changes_when_trip_is_updated(self):
        """
        Verify that updated_at changes when a trip is updated.
        """
        trip = Trip(
            name='Trip to test_updated_at_changes_when_trip_is_updated',
            city='Test',
            country=self.country,
            description='Trip to the city of tests',
            rating=5,
        )
        trip.save()
        trip.refresh_from_db()
        previous_updated_at = trip.updated_at
        trip.city = 'Test city'
        trip.save()
        trip.refresh_from_db()
        self.assertGreater(trip.updated_at, previous_updated_at)
