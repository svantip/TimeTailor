import random

from django.db import transaction
from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from main.models import UserProfile, Task, Category
from main.factory import (
    UserProfileFactory,
    TaskFactory,
    CategoryFactory,
)

NUM_INSTANCES = 3


class Command(BaseCommand):
    help = 'Generate test data for UserProfile, Task, and Category models.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Deleting old data...'))
        UserProfile.objects.all().delete()
        Task.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Creating new data...'))

        for _ in range(NUM_INSTANCES):
            UserProfileFactory()

        tasks = []
        for _ in range(NUM_INSTANCES):
            tasks.append(TaskFactory())

        for _ in range(NUM_INSTANCES):
            CategoryFactory()

        self.stdout.write(self.style.SUCCESS(f'Created {NUM_INSTANCES} instances for each model.'))