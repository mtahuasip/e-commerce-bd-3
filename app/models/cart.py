from datetime import datetime, timezone
from bson import ObjectId
from app.extensions import mongo
from app.models.user import User
from app.models.product import Product


class Cart:
    def __init__(
        self,
        _id=None,
        user_id=None,
        products=None,
        total=0.0,
        created_at=None,
        updated_at=None,
    ):
        self._id = _id
        self.user_id = ObjectId(user_id) if user_id else None
        self.products = products or []
        self.total = total
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def to_dict(self):
        cart_dict = {
            "user_id": self.user_id,
            "products": self.products,
            "total": self.total,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        if self._id:
            cart_dict["_id"] = str(self._id)
        return cart_dict

    @staticmethod
    def from_dict(data):
        return Cart(
            _id=ObjectId(data["_id"]) if "_id" in data else None,
            user_id=data["user_id"],
            products=data["products"],
            total=data["total"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

    @staticmethod
    def create_cart(user_id):
        cart = Cart(user_id=user_id)
        result = mongo.db.carts.insert_one(cart.to_dict())

        created_cart = mongo.db.carts.find_one({"_id": result.inserted_id})

        return Cart.from_dict(created_cart)

    @staticmethod
    def find_cart_by_user_id(user_id):
        cart_data = mongo.db.carts.find_one({"user_id": ObjectId(user_id)})

        if cart_data:
            return Cart.from_dict(cart_data), "Carrito encontrado", "success"

        return None, "Carrito no encontrado", "danger"

    @staticmethod
    def add_product(cart_id, product_id, quantity=1):
        try:
            product, message, category = Product.find_by_id(product_id)
            if not product:
                return message, category

            cart_data = mongo.db.carts.find_one({"_id": ObjectId(cart_id)})

            if not cart_data:
                return "Carrito no encontrado", "danger"

            cart = Cart.from_dict(cart_data)
            existing_item = next(
                (
                    item
                    for item in cart.products
                    if item["product"]["_id"] == product._id
                ),
                None,
            )

            if existing_item:
                existing_item["quantity"] += quantity
                existing_item["subtotal"] = round(
                    existing_item["quantity"] * product.price, 2
                )
            else:
                cart.products.append(
                    {
                        "product": product.to_dict(),
                        "quantity": quantity,
                        "subtotal": round(quantity * product.price, 2),
                    }
                )

            cart._recalculate_total()

            mongo.db.carts.update_one(
                {"_id": ObjectId(cart_id)},
                {
                    "$set": {
                        "products": cart.products,
                        "total": cart.total,
                        "updated_at": cart.updated_at,
                    }
                },
            )

            return "Producto agregado al carrito", "success"
        except:
            return "Error al agregar el producto", "danger"

    def _recalculate_total(self):
        self.total = sum(item["subtotal"] for item in self.products)
        self.updated_at = datetime.now(timezone.utc)
