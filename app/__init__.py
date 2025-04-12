from flask import Flask
from flask_login import LoginManager
from bson import ObjectId
import redis as PyRedis
from .extensions import mongo, redis
from .config import Config
from .init_indexes import create_indexes
from .models.user import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    create_indexes(mongo.db)

    global redis
    redis = PyRedis.Redis(
        host=app.config["REDIS_HOST"],
        port=app.config["REDIS_PORT"],
        db=0,
        decode_responses=True,
    )

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User.from_dict(user_data)
        return None

    from .routes.public_routes import public
    from .routes.auth_routes import auth
    from .routes.account_routes import account
    from .routes.cart_routes import cart

    app.register_blueprint(public)
    app.register_blueprint(auth)
    app.register_blueprint(account)
    app.register_blueprint(cart)

    return app
