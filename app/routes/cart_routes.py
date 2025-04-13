from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models.cart import Cart

cart = Blueprint("cart", __name__)


@cart.route("/add-product-to-cart", methods=["POST"])
@login_required
def add_product_to_cart():
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity")

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

    return render_template("cart/my_cart.html", show_sidebar=False, cart=cart)
