from flask import Blueprint, render_template, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.forms.auth_forms import (
    RegisterForm,
    LoginForm,
    ProfileForm,
    ChangePasswordForm,
)
from app.models.user import User

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/")

    form = RegisterForm()

    if form.validate_on_submit():
        message, category = User.create(data=form.data)
        flash(message, category)
        form.data.clear()

        if category == "success":
            return redirect("/login")

    return render_template("auth/register.html", show_sidebar=False, form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    form = LoginForm()

    if form.validate_on_submit():
        user, message, category = User.find_one_by_email(form.email.data)

        if not user:
            flash(message, category)
            form.data.clear()
            return render_template("auth/login.html", show_sidebar=False, form=form)

        message, category = user.verify_password(form.password.data)

        if category == "success":
            login_user(user)
            flash(message, category)
            form.data.clear()
            return redirect("/products")
        else:
            flash(message, category)

    return render_template("auth/login.html", show_sidebar=False, form=form)


@auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm()

    if form.validate_on_submit():
        id = current_user.id
        message, category = User.update(id, form.data)

        if category == "success":
            flash(message, category)
            form.data.clear()
            return redirect("/profile")
        else:
            flash(message, category)
            form.data.clear()

    return render_template(
        "auth/profile.html",
        show_sidebar=False,
        active_page="profile",
        form=form,
    )


@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        id = current_user.id
        message, category = User.update_password(id, form.data)

        if category == "success":
            flash(message, category)
            form.data.clear()
            return redirect("/change-password")
        else:
            flash(message, category)
            form.data.clear()

    return render_template(
        "auth/change_password.html",
        show_sidebar=False,
        active_page="change_password",
        form=form,
    )


@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect("/login")
