from country_list import countries_for_language
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.trips.models import Country


class Command(BaseCommand):
    help = 'Import countries into the database.'

    @transaction.atomic
    def handle(self, *args, **options):
        countries = countries_for_language('en')

        for code, name in countries:
            Country.objects.update_or_create(
                code=code,
                defaults={'name': name},
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'{len(countries)} countries imported or updated.'
            )
        )
