from datetime import datetime

from ...models import Post, Category
from comment.models import Comment
from django.core.management.base import BaseCommand, CommandError
from accounts.models import Profile, User
import faker
import random


categories = ["Tech", "AI", "Blockchain", "Machine Learning"]


class Command(BaseCommand):
    help = "Add dummy data - you have parse user email"

    def add_arguments(self, parser):
        parser.add_argument("user", nargs="+", type=str)

    def handle(self, *args, **options):
        user_email = options["user"][0]
        fake = faker.Faker()
        try:
            print("Faking the user's profile")
            user = User.objects.get(email=user_email)
            print("User found successfully.")
            profile = Profile.objects.get(user=user)
            profile.first_name = fake.first_name()
            profile.last_name = fake.last_name()
            profile.bio = fake.text()
            profile.save()
            print("Profile detail generated successfully.")

            print("=" * 15)

            print("Creating categories...")
            for c in categories:
                Category.objects.get_or_create(name=c)
            print("Categories created successfully.")

            print("=" * 15)

            print("Generating 10 posts with random details...")
            for _ in range(10):
                post = Post()
                post.title = fake.sentence()
                post.category = Category.objects.get(name=random.choice(categories))
                post.status = random.choice([True, False])
                post.slug = fake.slug()
                post.published_date = datetime.now()
                post.content = fake.text()
                post.author = profile
                post.save()
            print("Created posts successfully")

        except Profile.DoesNotExist:
            print("User can not be found")

        except Exception as e:
            print("Something went wrong:", e)


