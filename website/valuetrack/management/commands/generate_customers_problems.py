from django.core.management.base import BaseCommand
from faker import Faker
import random
from valuetrack.models import Customer, ProblemStatement  # adjust if your app name is different

class Command(BaseCommand):
    help = 'Generate 20 customers with problem statements'

    def handle(self, *args, **kwargs):
        fake = Faker()

        industry_choices = [choice[0] for choice in Customer._meta.get_field('industry').choices]
        location_choices = [choice[0] for choice in Customer._meta.get_field('location').choices]
        status_choices = [choice[0] for choice in Customer._meta.get_field('status').choices]
        urgency_choices = [choice[0] for choice in ProblemStatement._meta.get_field('urgency').choices]
        problem_status_choices = [choice[0] for choice in ProblemStatement._meta.get_field('status').choices]

        for _ in range(20):
            customer = Customer.objects.create(
                name=fake.company(),
                main_contact=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                industry=random.choice(industry_choices),
                location=random.choice(location_choices),
                account_manager=fake.name(),
                status=random.choice(status_choices),
                notes=fake.paragraph(nb_sentences=3),
            )

            for _ in range(random.randint(1, 3)):
                ProblemStatement.objects.create(
                    customer=customer,
                    title=fake.sentence(nb_words=6),
                    description=fake.paragraph(nb_sentences=4),
                    impact=fake.paragraph(nb_sentences=2),
                    urgency=random.choice(urgency_choices),
                    status=random.choice(problem_status_choices),
                    notes=fake.sentence(),
                )

        self.stdout.write(self.style.SUCCESS('✅ 20 customers with problem statements created.'))