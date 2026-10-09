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

    def test_index_uses_correct_template(self):
        """
        Index view uses the correct template.
        """
        response = self.client.get(reverse('trips:index'))
        self.assertTemplateUsed(response, 'trips/index.html')

    def test_index_passes_trips_in_context(self):
        """
        Index view uses the correct context for template.
        """
        trip1 = Trip.objects.create(
            name='Trip 1 to TripIndexViewTests',
            destination='Testland',
            description='A test trip description',
            rating=10,
        )
        trip2 = Trip.objects.create(
            name='Trip 2 to TripIndexViewTests',
            destination='Testland',
            description='A test trip description',
            rating=10,
        )
        self.assertEqual(Trip.objects.count(), 2)
        response = self.client.get(reverse('trips:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('trips', response.context)
        self.assertIn(trip1, response.context['trips'])
        self.assertIn(trip2, response.context['trips'])


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

    def test_create_trip_uses_correct_template(self):
        """
        Create view uses the correct template.
        """
        response = self.client.post(reverse('trips:create'), data={})
        self.assertTemplateUsed(response, 'trips/create.html')


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


class TripUpdateViewTests(TestCase):
    def setUp(self):
        self.trip = Trip.objects.create(
            name='Trip to TripUpdateViewTests',
            destination='Testland',
            start_date=datetime.date.today(),
            end_date=datetime.date.today(),
            description='A test trip description',
            status='completed',
            rating=10,
        )

    def test_trip_update_returns_200(self):
        """
        Update view returns 200 when the trip exists.
        """
        response = self.client.get(reverse('trips:update', kwargs={'pk': self.trip.pk}))
        self.assertEqual(response.status_code, 200)

    def test_trip_update_returns_404_for_unknown_trip(self):
        """
        Update view returns 404 when the trip does not exist.
        """
        response = self.client.get(reverse('trips:update', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_trip_update_uses_correct_template(self):
        """
        Update view uses the correct template.
        """
        response = self.client.get(reverse('trips:update', kwargs={'pk': self.trip.pk}))
        self.assertTemplateUsed(response, 'trips/update.html')

    def test_trip_update_passes_trip_in_context(self):
        """
        Update view uses the correct context for template.
        """
        response = self.client.get(reverse('trips:update', kwargs={'pk': self.trip.pk}))
        self.assertEqual(response.context['trip'], self.trip)

    def test_trip_update_form_is_prefilled(self):
        """
        Update form is prefilled.
        """
        response = self.client.get(reverse('trips:update', kwargs={'pk': self.trip.pk}))
        self.assertEqual(response.context['form'].instance, self.trip)
        self.assertEqual(response.context['form']['name'].value(), self.trip.name)
        self.assertEqual(response.context['form']['destination'].value(), self.trip.destination)
        self.assertEqual(response.context['form']['start_date'].value(), self.trip.start_date)
        self.assertEqual(response.context['form']['end_date'].value(), self.trip.end_date)
        self.assertEqual(response.context['form']['description'].value(), self.trip.description)
        self.assertEqual(response.context['form']['status'].value(), self.trip.status)
        self.assertEqual(response.context['form']['rating'].value(), self.trip.rating)

    def test_trip_update_with_valid_data(self):
        """
        Update view with valid data.
        """
        response = self.client.post(reverse('trips:update', kwargs={'pk': self.trip.pk}), data={
            'name': 'Updated trip',
            'destination': 'Testlandia',
            'description': 'Updated description',
            'start_date': '2026-10-09',
            'end_date': '2026-10-09',
            'rating': 0,
            'status': 'cancelled',
        })
        self.assertEqual(response.status_code, 302)
        self.trip.refresh_from_db()
        self.assertEqual(self.trip.name, 'Updated trip')
        self.assertEqual(self.trip.destination, 'Testlandia')
        self.assertEqual(self.trip.description, 'Updated description')
        self.assertEqual(self.trip.start_date, datetime.date(2026, 10, 9))
        self.assertEqual(self.trip.end_date, datetime.date(2026, 10, 9))
        self.assertEqual(self.trip.rating, 0)
        self.assertEqual(self.trip.status, 'cancelled')
        self.assertEqual(Trip.objects.count(), 1)

    def test_trip_update_with_invalid_data(self):
        """
        Update view with invalid data.
        """
        original_name = self.trip.name
        response = self.client.post(reverse('trips:update', kwargs={'pk': self.trip.pk}), data={
            'name': '',
            'destination': 'Testlandia',
            'description': 'Updated description',
            'start_date': '2026-10-18',
            'end_date': '2026-10-15',
            'rating': -9999,
            'status': 'invalid',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.trip.refresh_from_db()
        self.assertEqual(self.trip.name, original_name)
        self.assertEqual(Trip.objects.count(), 1)


class TripDeleteViewTests(TestCase):
    def setUp(self):
        self.trip = Trip.objects.create(
            name='Trip to TripDeleteViewTests',
            destination='Testland',
            description='A test trip description',
            rating=10,
        )

    def test_delete_trip_returns_200(self):
        """
        Delete view returns 200.
        """
        response = self.client.get(reverse('trips:delete', kwargs={'pk': self.trip.pk}))
        self.assertEqual(response.status_code, 200)
