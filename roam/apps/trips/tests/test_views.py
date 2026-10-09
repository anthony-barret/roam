import datetime

from django.test import TestCase
from django.urls import reverse

from apps.trips.models import Trip


class TripIndexViewTests(TestCase):
    def test_no_trip(self):
        """
        If no trips exist, the message 'Please add a trip !' is displayed.
        """
        response = self.client.get(reverse('trips:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please add a trip !')

    def test_at_least_one_trip(self):
        """
        If there is at least one trip, the message 'Please add a trip !' is not displayed.
        """
        trip = Trip.objects.create(
            name='Trip to Testland',
            destination='Testland',
            rating=10,
            status='completed',
        )
        response = self.client.get(reverse('trips:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Please add a trip !')


class TripCreateViewTests(TestCase):
    def test_create_trip_valid_parameters(self):
        """
        Create a trip with valid parameters
        """
        response = self.client.post(reverse('trips:create'), data={
            'name': 'Trip to test_create_trip_valid_parameters',
            'destination': 'Testland',
            'start_date': datetime.date.today(),
            'end_date': datetime.date.today(),
            'description': 'Trip to Testland',
            'rating': 10,
            'status': 'completed',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Trip.objects.count(), 1)
        trip = Trip.objects.get(name='Trip to test_create_trip_valid_parameters')
        self.assertEqual(trip.destination, 'Testland')
        self.assertEqual(trip.start_date, datetime.date.today())
        self.assertEqual(trip.end_date, datetime.date.today())
        self.assertEqual(trip.description, 'Trip to Testland')
        self.assertEqual(trip.rating, 10)
        self.assertEqual(trip.status, 'completed')
