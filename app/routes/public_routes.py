from flask import Blueprint, render_template, flash, redirect, request
from datetime import datetime, timedelta, timezone
from app.models.category import Category

public = Blueprint("public", __name__)


@public.route("/", methods=["GET"])
def home():
    return render_template("public/home.html", show_sidebar=False, active_page="home")


@public.route("/products", methods=["GET"])
def products():

    return render_template(
        "public/products.html", show_sidebar=True, active_page="products"
    )


@public.route("/categories", methods=["GET"])
def categories():
    sort = request.args.get("sort")
    last_week = (datetime.now(timezone.utc) - timedelta(days=7)).replace(tzinfo=None)

    categories, message, category = Category.find_all(sort)

    if category == "danger":
        flash(message, category)
        return redirect("/")

    return render_template(
        "public/categories.html",
        show_sidebar=True,
        active_page="categories",
        categories=categories,
        last_week=last_week,
        sort=sort,
    )
