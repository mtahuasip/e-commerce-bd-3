from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    FloatField,
    PasswordField,
    EmailField,
    BooleanField,
    SubmitField,
    SelectField,
)
from wtforms.validators import DataRequired, length


class RegisterForm(FlaskForm):
    name = StringField("Nombre completo", validators=[DataRequired()])
    email = EmailField("Correo electrónico", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired(), length(min=8)])
    password_confirm = PasswordField(
        "Confirmar contraseña",
        validators=[DataRequired(), length(min=8)],
    )
    submit = SubmitField("Registrarse")


class LoginForm(FlaskForm):
    email = EmailField("Correo electrónico", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired(), length(min=8)])
    submit = SubmitField("Entrar")


class ProfileForm(FlaskForm):
    name = StringField("Nombre completo", validators=[DataRequired()])
    email = EmailField("Correo electrónico", validators=[DataRequired()])
    submit = SubmitField("Guardar")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Contraseña actual",
        validators=[DataRequired(), length(min=8)],
    )
    new_password = PasswordField(
        "Nueva contraseña",
        validators=[DataRequired(), length(min=8)],
    )
    password_confirm = PasswordField(
        "Confirmar nueva contraseña",
        validators=[DataRequired(), length(min=8)],
    )
    submit = SubmitField("Guardar cambios")
