from flask import Flask
from flask_pymongo import PyMongo
from .config import Config
from .init_indexes import create_indexes

# Instancia de MongoDB
mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Se inicializa la conexión a MongoDB
    mongo.init_app(app)
    create_indexes(mongo.db)

    from .routes.public_routes import public
    from .routes.auth_routes import auth
    from .routes.account_routes import account
    from .routes.cart_routes import cart

    app.register_blueprint(public)  # url_prefix="/"
    app.register_blueprint(auth)  # url_prefix="/auth"
    app.register_blueprint(account)  # url_prefix="/account"
    app.register_blueprint(cart)  # url_prefix="/cart"

    return app
