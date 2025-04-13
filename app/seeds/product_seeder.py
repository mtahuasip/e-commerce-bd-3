import sys, os
import random
from faker import Faker
from bson import ObjectId

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.models.category import Category
from app.models.product import Product

fake = Faker()


def seed_products(num_categories=10):
    categories, _, _ = Category.find_all()

    if not categories:
        print("No hay categorías para asignar productos.")
        return

    for _ in range(num_categories):
        category = random.choice(categories)

        Product.create(
            {
                "name": fake.unique.word().capitalize()
                + " "
                + fake.word().capitalize(),
                "description": fake.sentence(),
                "price": round(random.uniform(10.0, 1000.0), 2),
                "stock": random.randint(0, 100),
                "image_url": fake.image_url(),
                "category_id": str(category._id),
            }
        )
