import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from faker import Faker
from app.models.category import Category

fake = Faker()


def seed_categories(num_categories=10):
    for _ in range(num_categories):
        Category.create(
            {
                "name": " ".join(word.capitalize() for word in fake.words(nb=3)),
                "image_url": fake.image_url(),
            }
        )
