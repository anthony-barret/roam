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
