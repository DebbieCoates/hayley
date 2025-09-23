from django.core.management.base import BaseCommand
from valuetrack.models import Customer
from faker import Faker
import random

fake = Faker()

INDUSTRY_CHOICES = [choice[0] for choice in Customer._meta.get_field('industry').choices]
LOCATION_CHOICES = [choice[0] for choice in Customer._meta.get_field('location').choices]
STATUS_CHOICES = [choice[0] for choice in Customer._meta.get_field('status').choices]

class Command(BaseCommand):
    help = 'Generate fake customers for testing'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Number of customers to create')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for _ in range(total):
            Customer.objects.create(
                name=fake.company(),
                main_contact=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                industry=random.choice(INDUSTRY_CHOICES),
                location=random.choice(LOCATION_CHOICES),
                account_manager=fake.name(),
                status=random.choice(STATUS_CHOICES),
                notes=fake.paragraph(nb_sentences=3),
                archived=random.choice([True, False])
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} customers'))