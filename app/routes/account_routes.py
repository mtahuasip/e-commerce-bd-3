from flask import Blueprint, render_template
from flask_login import current_user


account = Blueprint("account", __name__)


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
