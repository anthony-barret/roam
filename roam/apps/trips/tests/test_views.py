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
        Create a trip with valid parameters.
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

    def test_create_trip_invalid_parameters(self):
        """
        Create a trip with invalid parameters.
        """
        response = self.client.post(reverse('trips:create'), data={
            'name': 'Trip to test_create_trip_invalid_parameters',
            'start_date': datetime.date(2026, 10, 11),
            'end_date': datetime.date(2026, 10, 9),
            'description': 'Trip to Testland',
            'rating': -10,
            'status': 'invalid',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('end_date', response.context['form'].errors)
        self.assertIn('rating', response.context['form'].errors)
        self.assertIn('status', response.context['form'].errors)
        self.assertEqual(Trip.objects.count(), 0)


class TripDetailViewTests(TestCase):
    def setUp(self):
        self.trip = Trip.objects.create(
            name='Trip to TripDetailViewTests',
            destination='Testland',
            description='A test trip description',
            rating=10,
        )

    def test_trip_detail_returns_200(self):
        """
        Detail view returns 200 when the trip exists.
        """
        response = self.client.get(reverse('trips:detail', kwargs={'pk': self.trip.pk}))
        self.assertEqual(response.status_code, 200)

    def test_trip_detail_returns_404_for_unknown_trip(self):
        """
        Detail view returns 404 when the trip does not exist.
        """
        response = self.client.get(reverse('trips:detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_trip_detail_displays_trip_information(self):
        """
        Detail view displays trip information.
        """
        response = self.client.get(reverse('trips:detail', kwargs={'pk': self.trip.pk}))
        self.assertContains(response, self.trip.name)
        self.assertContains(response, self.trip.destination)
        self.assertContains(response, self.trip.description)

    def test_trip_detail_uses_correct_template(self):
        """
        Detail view uses the correct template.
        """
        response = self.client.get(reverse('trips:detail', kwargs={'pk': self.trip.pk}))
        self.assertTemplateUsed(response, 'trips/detail.html')

    def test_trip_detail_passes_trip_in_context(self):
        """
        Detail view uses the correct context for template.
        """
        response = self.client.get(reverse('trips:detail', kwargs={'pk': self.trip.pk}))
        self.assertEqual(response.context['trip'], self.trip)
