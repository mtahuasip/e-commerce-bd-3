from flask import Blueprint, render_template, flash, redirect, request
from datetime import datetime, timedelta, timezone
from app.models.category import Category
from app.models.product import Product

public = Blueprint("public", __name__)


@public.route("/", methods=["GET"])
def home():
    return render_template("public/home.html", show_sidebar=False, active_page="home")


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


@public.route("/products", methods=["GET"])
def products():
    sort = request.args.get("sort")
    category_name = request.args.get("category")
    last_week = (datetime.now(timezone.utc) - timedelta(days=7)).replace(tzinfo=None)

    categories, message, category = Category.find_all("a-z")

    if category == "danger":
        flash(message, category)
        return redirect("/")

    products, message, category = Product.find_all(sort, category_name)

    if category == "danger":
        flash(message, category)
        return redirect("/")

    return render_template(
        "public/products.html",
        show_sidebar=True,
        active_page="products",
        categories=categories,
        products=products,
        last_week=last_week,
        sort=sort,
        category_name=category_name,
    )
