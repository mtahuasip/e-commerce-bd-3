from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo


class User:
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
    def password(self):
        raise AttributeError("La contraseña es un atributo que no se puede leer")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        user_dict = {
            "name": self.name,
            "email": self.email,
            # "password_hash": self.password_hash,
            "is_admin": self.is_admin,
            "is_staff": self.is_staff,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

        if self._id:
            user_dict["_id"] = str(self._id)

        return user_dict

    @staticmethod
    def from_dict(data):
        return User(
            _id=data["_id"] if "_id" in data else None,
            name=data["name"],
            email=data["email"],
            password_hash=data["password_hash"],
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
