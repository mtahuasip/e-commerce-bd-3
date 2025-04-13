import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app import create_app
from app.seeds.category_seeder import seed_categories
from app.seeds.product_seeder import seed_products


app = create_app()
with app.app_context():

    def run():
        seed_categories(20)
        seed_products(100)
        print("Seeding completado")

    if __name__ == "__main__":
        run()
