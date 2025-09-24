from django.core.management.base import BaseCommand
from faker import Faker
from valuetrack.models import Provider
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Seed the database with fake providers for development'

    def handle(self, *args, **kwargs):
        fake = Faker('en_GB')  # UK-specific formatting
        types = ['Internal', 'External', 'Partner']
        statuses = ['Active', 'Inactive']
        countries = ['United Kingdom', 'France', 'Germany', 'United States', 'Canada']

        # Use first user as creator (or None if no users exist)
        user = User.objects.first()

        for _ in range(50):  # Adjust count as needed
            provider_type = random.choice(types)
            department = fake.company() if provider_type == 'Internal' else None

            Provider.objects.create(
                name=fake.company(),
                type=provider_type,
                department=department,
                contact_name=fake.name(),
                email=fake.company_email(),
                phone=fake.phone_number(),
                address=fake.street_address(),
                address2=fake.secondary_address(),
                city=fake.city(),
                county=fake.county(),
                postcode=fake.postcode(),
                country=random.choice(countries),
                notes=fake.paragraph(nb_sentences=2),
                status=random.choice(statuses),
                tags=", ".join(fake.words(nb=3)),
                created_by=user
            )

        self.stdout.write(self.style.SUCCESS('✅ Successfully seeded 50 providers'))