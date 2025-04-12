from flask import Blueprint, render_template

account = Blueprint("account", __name__)


@account.route("/profile", methods=["GET"])
def profile():
    return render_template(
        "account/profile.html", show_sidebar=False, active_page="profile"
    )


@account.route("/orders", methods=["GET"])
def orders():
    return render_template(
        "account/orders.html", show_sidebar=False, active_page="orders"
    )


@account.route("/purchases", methods=["GET"])
def purchases():
    return render_template(
        "account/purchases.html", show_sidebar=False, active_page="purchases"
    )
