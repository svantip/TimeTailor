
import random
import factory
from factory.django import DjangoModelFactory
from factory import SubFactory, post_generation
from django.contrib.auth.models import User
from .models import UserProfile, Task, Category
import datetime
from factory import fuzzy

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')

class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = SubFactory(UserFactory)

class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('sentence', nb_words=1)
    icon = factory.Iterator(['bxs-coffee', 'bxs-book', 'bxs-briefcase'])
    color = factory.Faker('hex_color')
    start_time = factory.Faker('time_object')
    duration = factory.LazyFunction(lambda: datetime.timedelta(minutes=random.randint(15, 120)))
    repeat_frequency = fuzzy.FuzzyChoice(choices=[None, 'daily', 'weekly'])
    is_quick_add = factory.Faker('boolean')
    is_completed = False
    date = fuzzy.FuzzyDate(start_date=datetime.date(2020, 1, 1))

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    user = SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Category {n}")
    description = factory.Faker('paragraph', nb_sentences=3)

    @post_generation
    def tasks(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for task in extracted:
                self.task.add(task)