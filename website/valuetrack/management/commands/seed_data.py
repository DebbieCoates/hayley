from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from valuetrack.models import (
    Customer, ProblemStatement, Provider, Category,
    Service, Solution, ProblemSolutionLink
)
from faker import Faker
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seed test data for Customer, ProblemStatement, Provider, Category, Service, Solution, and ProblemSolutionLink'

    def handle(self, *args, **kwargs):
        fake = Faker()
        user = User.objects.first()

        # Create Categories
        categories = []
        for _ in range(5):
            category = Category.objects.create(
                name=fake.unique.word().capitalize(),
                description=fake.sentence()
            )
            categories.append(category)

        # Create Services
        services = []
        for _ in range(10):
            service = Service.objects.create(
                name=fake.bs().title(),
                description=fake.text(max_nb_chars=150),
                category=random.choice(categories),
                tags=",".join(fake.words(nb=3)),
                active=True,
                created_by=user
            )
            services.append(service)

        # Create Providers
        providers = []
        for _ in range(10):
            provider = Provider.objects.create(
                name=fake.company(),
                type=random.choice(['Internal', 'External', 'Partner']),
                department=fake.bs(),
                contact_name=fake.name(),
                email=fake.company_email(),
                phone=fake.phone_number(),
                address=fake.street_address(),
                address2=fake.secondary_address(),
                city=fake.city(),
                county=fake.state(),
                postcode=fake.postcode(),
                country=fake.country(),
                notes=fake.text(max_nb_chars=100),
                status=random.choice(['Active', 'Inactive']),
                website=fake.url(),
                industry=random.choice(['Tech', 'Finance', 'Health', 'Edu', 'Retail', 'Eng', 'Auto', 'Food', 'Media', 'Con', 'Other']),
                tags=",".join(fake.words(nb=3)),
                created_by=user
            )
            providers.append(provider)

        # Create Customers
        customers = []
        for _ in range(5):
            customer = Customer.objects.create(
                name=fake.company(),
                main_contact=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                industry=random.choice(['Tech', 'Finance', 'Health', 'Edu', 'Retail', 'Eng', 'Auto', 'Food', 'Media', 'Con', 'Other']),
                location=random.choice(['London', 'North West', 'South East', 'Scotland', 'Wales']),
                account_manager=fake.name(),
                status=random.choice(['Active', 'Inactive', 'Pending']),
                notes=fake.text(max_nb_chars=100)
            )
            customers.append(customer)

        # Create ProblemStatements
        problems = []
        for _ in range(10):
            problem = ProblemStatement.objects.create(
                customer=random.choice(customers),
                title=fake.catch_phrase(),
                description=fake.text(max_nb_chars=200),
                impact=fake.text(max_nb_chars=100),
                urgency=random.choice(['Low', 'Medium', 'High', 'Critical']),
                status=random.choice(['Open', 'In Progress', 'Resolved', 'Closed']),
                notes=fake.text(max_nb_chars=100)
            )
            problems.append(problem)

        # Create Solutions
        solutions = []
        for _ in range(15):
            solution = Solution.objects.create(
                name=fake.bs().title(),
                description=fake.text(max_nb_chars=150),
                service=random.choice(services),
                tags=",".join(fake.words(nb=3)),
                budget_eligible=random.choice([True, False]),
                created_by=user
            )
            solution.providers.set(random.sample(providers, k=random.randint(1, 3)))
            solutions.append(solution)

        # Link Problems to Solutions
        for _ in range(20):
            ProblemSolutionLink.objects.create(
                problem=random.choice(problems),
                solution=random.choice(solutions),
                notes=fake.sentence()
            )

        self.stdout.write(self.style.SUCCESS('✅ Seeded test data for all models.'))