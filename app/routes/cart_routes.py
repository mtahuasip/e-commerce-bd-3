from flask import Blueprint, render_template

cart = Blueprint("cart", __name__)


@cart.route("/view", methods=["GET"])
def view():
    return render_template("cart/view.html", show_sidebar=False)
