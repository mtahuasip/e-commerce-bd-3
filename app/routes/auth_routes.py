from flask import Blueprint, render_template, redirect

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET"])
def login():
    return render_template("auth/login.html", show_sidebar=False)


@auth.route("/register", methods=["GET"])
def register():
    return render_template("auth/register.html", show_sidebar=False)


@auth.route("/change-password", methods=["GET"])
def change_password():
    return render_template(
        "auth/change_password.html", show_sidebar=False, active_page="change_password"
    )


@auth.route("/edit-profile", methods=["GET"])
def edit_profile():
    return render_template(
        "auth/edit_profile.html", show_sidebar=False, active_page="edit_profile"
    )


@auth.route("/logout", methods=["GET"])
def logout():
    return redirect("/login")
