from datetime import datetime, timezone
from bson import ObjectId
from app.extensions import mongo
from slugify import slugify


class Category:
    def __init__(
        self,
        _id=None,
        name=None,
        image_url=None,
        slug=None,
        products=None,
        created_at=None,
        updated_at=None,
    ):
        self._id = _id
        self.name = name
        self.image_url = image_url
        self.slug = slug or slugify(name) if name else None
        self.products = products or []
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def __str__(self):
        return f"<Category {self._id}>"

    def to_dict(self):
        category_dict = {
            "name": self.name,
            "image_url": self.image_url,
            "slug": self.slug,
            "products": self.products,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

        if self._id:
            category_dict["_id"] = str(self._id)

        return category_dict

    @staticmethod
    def from_dict(data):
        return Category(
            _id=ObjectId(data["_id"]) if "_id" in data else None,
            name=data["name"],
            image_url=data["image_url"],
            slug=data["slug"],
            products=data["products"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

    @staticmethod
    def create(data):
        try:
            name = data["name"]

            if mongo.db.categories.find_one({"name": name}):
                return "La categoría ya existe", "warning"

            category = Category(name=data["name"], image_url=data["image_url"])
            mongo.db.categories.insert_one(category.to_dict())

            return "Categoría creada correctamente", "success"

        except Exception as e:
            return f"Error al crear categoría: {e}", "danger"

    @staticmethod
    def find_by_id(id):
        try:
            category = mongo.db.categories.find_one({"_id": ObjectId(id)})

            if category:
                return Category.from_dict(category), None, "success"

            return None, "Categoría no encontrada", "danger"
        except Exception as e:
            return None, f"Error al buscar categoría: {e}", "danger"

    @staticmethod
    def find_all(option=None):
        try:
            sort_option = None

            if option == "az":
                sort_option = [("name", 1)]
            elif option == "za":
                sort_option = [("name", -1)]
            elif option == "recent":
                sort_option = [("created_at", -1)]

            categories_cursor = mongo.db.categories.find()
            if sort_option:
                categories_cursor = categories_cursor.sort(sort_option)

            categories = [
                Category.from_dict(category) for category in categories_cursor
            ]

            return categories, None, "success"

        except Exception as e:
            return [], f"Error al buscar categorías: {e}", "danger"
