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
    help = 'Populate the database with sample data for UserProfile, Task, and Category models.'

    @transaction.atomic
    def handle(self, *args, **options):
        # Clear existing data
        print('Deleting old data...')
        Category.objects.all().delete()
        Task.objects.all().delete()
        UserProfile.objects.all().delete()

        # Create new data
        print('Creating new data...')
        user_profiles = UserProfileFactory.create_batch(NUM_INSTANCES)
        tasks = TaskFactory.create_batch(NUM_INSTANCES)
        categories = CategoryFactory.create_batch(NUM_INSTANCES, tasks=random.sample(tasks, k=2))  # Assign some tasks to each category

        print(f'Created {len(user_profiles)} user profiles, {len(tasks)} tasks, and {len(categories)} categories.')