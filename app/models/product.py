from datetime import datetime, timezone
from bson import ObjectId
from slugify import slugify
from app.extensions import mongo
from app.models.category import Category


class Product:
    def __init__(
        self,
        _id=None,
        name=None,
        description=None,
        price=1.0,
        stock=0,
        image_url=None,
        slug=None,
        category_id=None,
        created_at=None,
        updated_at=None,
    ):
        self._id = _id
        self.name = name
        self.description = description
        self.price = float(price)
        self.stock = int(stock)
        self.image_url = image_url
        self.slug = slug or slugify(name) if name else None
        self.category_id = category_id
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def __str__(self):
        return f"<Product {self._id}>"

    def to_dict(self):
        product_dict = {
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "image_url": self.image_url,
            "slug": self.slug,
            "category_id": self.category_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

        if self._id:
            product_dict["_id"] = ObjectId(self._id)

        return product_dict

    @staticmethod
    def from_dict(data):
        return Product(
            _id=ObjectId(data["_id"]) if "_id" in data else None,
            name=data["name"],
            description=data["description"],
            price=data["price"],
            stock=data["stock"],
            image_url=data["image_url"],
            slug=data["slug"],
            category_id=data["category_id"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

    @staticmethod
    def create(data):
        try:
            name = data["name"]
            category_id = data["category_id"]
            category, _, _ = Category.find_by_id(category_id)

            if not category:
                return "Categoría no encontrada", "danger"

            if mongo.db.products.find_one({"name": name}):
                return "El producto ya existe", "warning"

            product = Product(
                name=data["name"],
                description=data["description"],
                price=data["price"],
                stock=data["stock"],
                image_url=data["image_url"],
                category_id=category._id,
            )

            result = mongo.db.products.insert_one(product.to_dict())
            Category.add_product(
                category_id=category._id, product_id=result.inserted_id
            )

            return "Producto creado correctamente", "success"

        except Exception as e:
            return f"Error al crear producto: {e}", "danger"

    @staticmethod
    def find_by_id(id):
        try:
            product = mongo.db.products.find_one({"_id": ObjectId(id)})

            if product:
                return Product.from_dict(product), None, "success"

            return None, "Producto no encontrado", "danger"
        except Exception as e:
            return None, f"Error al buscar producto: {e}", "danger"

    @staticmethod
    def find_by_slug(slug):
        try:
            product = mongo.db.products.find_one({"slug": slug})

            if product:
                return Product.from_dict(product), None, "success"

            return None, "Producto no encontrado", "danger"
        except Exception as e:
            return None, f"Error al buscar producto: {e}", "danger"

    @staticmethod
    def find_all(sort=None, category_name=None):
        try:
            query = {}
            if category_name:
                category, _, _ = Category.find_by_slug(category_name)

                if not category:
                    return None, "Categoría no encontrada", "danger"

                query["category_id"] = category._id

            products = mongo.db.products.find(query)

            if sort == "a-z":
                products = products.sort("name", 1)
            elif sort == "z-a":
                products = products.sort("name", -1)
            elif sort == "price-asc":
                products = products.sort("price", 1)
            elif sort == "price-desc":
                products = products.sort("price", -1)
            elif sort == "newest":
                products = products.sort("created_at", -1)
            elif sort == "oldest":
                products = products.sort("created_at", 1)

            return [Product.from_dict(product) for product in products], None, "success"

        except Exception as e:
            return None, f"Error al buscar productos: {e}", "danger"
