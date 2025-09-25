from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from valuetrack.models import Customer, ProblemStatement, Provider
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with test Customers, ProblemStatements, and Providers'

    def handle(self, *args, **kwargs):
        created_by_user = User.objects.first()

        # Create Providers
        for _ in range(15):
            Provider.objects.create(
                name=fake.company(),
                type=random.choice(['Internal', 'External', 'Partner']),
                department=fake.bs().title(),
                contact_name=fake.name(),
                email=fake.company_email(),
                phone=fake.phone_number(),
                address=fake.street_address(),
                address2=fake.secondary_address(),
                city=fake.city(),
                county=fake.state(),
                postcode=fake.postcode(),
                country=fake.country(),
                notes=fake.text(max_nb_chars=200),
                status=random.choice(['Active', 'Inactive']),
                website=fake.url(),
                industry=random.choice(['Tech', 'Finance', 'Health', 'Edu', 'Retail', 'Eng', 'Auto', 'Food', 'Media', 'Con', 'Other']),
                tags=", ".join(fake.words(nb=3)),
                created_by=created_by_user
            )

        # Create Customers and ProblemStatements
        for _ in range(10):
            customer = Customer.objects.create(
                name=fake.company(),
                main_contact=fake.name(),
                email=fake.company_email(),
                phone=fake.phone_number(),
                industry=random.choice(['Tech', 'Finance', 'Health', 'Edu', 'Retail', 'Eng', 'Auto', 'Food', 'Media', 'Con', 'Other']),
                location=random.choice(['East of England', 'East Midlands', 'London', 'North East', 'North West', 'South East', 'South West', 'West Midlands', 'Yorkshire and the Humber', 'Scotland', 'Wales', 'Northern Ireland', 'Other']),
                account_manager=fake.name(),
                status=random.choice(['Active', 'Inactive', 'Pending', 'Archived', 'Prospect', 'Other']),
                notes=fake.text(max_nb_chars=200)
            )

            for _ in range(random.randint(1, 3)):
                ProblemStatement.objects.create(
                    customer=customer,
                    title=fake.catch_phrase(),
                    description=fake.paragraph(nb_sentences=3),
                    impact=fake.paragraph(nb_sentences=2),
                    urgency=random.choice(['Low', 'Medium', 'High', 'Critical']),
                    status=random.choice(['Open', 'In Progress', 'Resolved', 'Closed']),
                    notes=fake.text(max_nb_chars=150)
                )

        self.stdout.write(self.style.SUCCESS('✅ Test data seeded successfully!'))