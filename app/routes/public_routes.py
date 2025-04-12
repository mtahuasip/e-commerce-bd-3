from flask import Blueprint, render_template

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
    return render_template(
        "public/categories.html", show_sidebar=True, active_page="categories"
    )
