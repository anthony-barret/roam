from django.test import TestCase
from django.urls import reverse


class TripIndexViewTests(TestCase):
    def test_no_trip(self):
        """
        If no trips exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('trips:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please add a trip !')
