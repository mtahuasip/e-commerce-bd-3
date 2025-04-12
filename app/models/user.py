from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from app.extensions import mongo


class User(UserMixin):
    def __init__(
        self,
        _id=None,
        name=None,
        email=None,
        password_hash=None,
        is_admin=False,
        is_staff=False,
        created_at=None,
        updated_at=None,
    ):
        self._id = _id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.is_staff = is_staff
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    @property
    def id(self):
        return str(self._id) if self._id else None

    @property
    def password(self):
        raise AttributeError("La contraseña es un atributo que no se puede leer")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        if check_password_hash(self.password_hash, password):
            return "Inicio de sesión exitoso", "success"
        else:
            return "Contraseña incorrecta", "danger"

    def to_dict(self):
        user_dict = {
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash,
            "is_admin": self.is_admin,
            "is_staff": self.is_staff,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

        if self._id:
            user_dict["_id"] = str(self._id)

        return user_dict

    @staticmethod
    def from_dict(data, password=False):
        return User(
            _id=ObjectId(data["_id"]) if "_id" in data else None,
            name=data["name"],
            email=data["email"],
            password_hash=data["password_hash"] if password else None,
            is_admin=data["is_admin"],
            is_staff=data["is_staff"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

    def __str__(self):
        return f"<User {self.email}>"

    @staticmethod
    def create(data):
        if data["password"] != data["password_confirm"]:
            return "Las contraseñas no coinciden", "warning"
        try:
            email = data["email"]
            if mongo.db.users.find_one({"email": email}):
                return "El correo electrónico ya está en uso", "warning"

            user = User(name=data["name"], email=email)
            user.password = data["password_confirm"]
            mongo.db.users.insert_one(user.to_dict())

            return "Usuario creado correctamente", "success"

        except Exception as e:
            return f"Error al crear usuario: {e}", "danger"

    @staticmethod
    def find_user_by_id(id):
        user = mongo.db.users.find_one({"_id": ObjectId(id)})
        if user:
            return User.from_dict(user, True), None, "success"
        return None, "Usuario no encontrado", "danger"

    @staticmethod
    def find_user_by_email(email):
        user = mongo.db.users.find_one({"email": email})
        if user:
            return User.from_dict(user, True), None, "success"
        return None, "Usuario no encontrado", "danger"

    @staticmethod
    def update(id, data):
        try:
            if not mongo.db.users.find_one({"_id": ObjectId(id)}):
                return "Usuario no encontrado", "danger"

            email = data["email"]
            if mongo.db.users.find_one({"email": email, "_id": {"$ne": ObjectId(id)}}):
                return "El correo electrónico ya está en uso", "warning"

            mongo.db.users.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                        "name": data["name"],
                        "email": email,
                        "updated_at": datetime.now(timezone.utc),
                    }
                },
            )

            return "Usuario actualizado correctamente", "success"

        except Exception as e:
            return f"Error al actualizar usuario: {e}", "danger"

    @staticmethod
    def update_password(id, data):
        try:
            user = mongo.db.users.find_one({"_id": ObjectId(id)})
            if not user:
                return "Usuario no encontrado", "danger"

            user = User.from_dict(user, True)
            message, category = user.verify_password(data["current_password"])

            if category == "danger":
                return message, category

            if data["new_password"] != data["password_confirm"]:
                return "Las nuevas contraseñas no coinciden", "warning"

            user.password = data["password_confirm"]

            mongo.db.users.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                        "password_hash": user.password_hash,
                        "updated_at": datetime.now(timezone.utc),
                    }
                },
            )

            return "Contraseña actualizada correctamente", "success"

        except Exception as e:
            return f"Error al actualizar contraseña: {e}", "danger"
