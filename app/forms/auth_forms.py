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
    password = PasswordField("Contraseña", validators=[DataRequired(), length(min=6)])
    password_confirm = PasswordField(
        "Confirmar contraseña", validators=[DataRequired(), length(min=6)]
    )
    submit = SubmitField("Registrarse")
