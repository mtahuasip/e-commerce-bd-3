from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required, current_user
from app.models.cart import Cart
from app.extensions import redis
from app.config import Config

cart = Blueprint("cart", __name__)


@cart.route("/add-product-to-cart", methods=["POST"])
@login_required
def add_product_to_cart():
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity")) or 1

    key = f"cart:{current_user.id}"

    current_qty = redis.hget(key, product_id)
    if current_qty:
        new_qty = int(current_qty) + quantity
    else:
        new_qty = quantity

    redis.hset(key, product_id, new_qty)

    redis.expire(key, Config.CART_DURATION)

    cart, _, _ = Cart.find_cart_by_user_id(current_user.id)

    if not cart:
        cart = Cart.create_cart(user_id=current_user.id)

    message, category = Cart.add_product(
        cart_id=cart._id, product_id=product_id, quantity=quantity
    )

    if category == "success":
        flash(message, category)
        return redirect("/products")

    return redirect("/products")


@cart.route("/my-cart", methods=["GET"])
@login_required
def my_cart():
    cart, message, category = Cart.find_cart_by_user_id(current_user.id)

    if category == "error":
        flash(message, category)
        return redirect("/products")

    if cart:
        key = f"cart:{current_user.id}"
        for item in cart.products:
            product_id = item["product"]["_id"]
            current_prod = redis.hget(key, str(product_id))

            if not current_prod:
                _, _ = Cart.delete_cart_by_user_id(current_user.id)
                cart = None

    return render_template("cart/my_cart.html", show_sidebar=False, cart=cart)
