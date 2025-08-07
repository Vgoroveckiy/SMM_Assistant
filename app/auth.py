from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import EqualTo, InputRequired, Length, ValidationError

from app import bcrypt, db
from app.models import User

auth_bp = Blueprint("auth", __name__)


class RegisterForm(FlaskForm):
    """
    Форма регистрации пользователей на Flask.

    Форма включает в себя поля для ввода имени пользователя, пароля, подтверждения пароля и кнопки отправки.
    Также она включает в себя валидацию, чтобы убедиться, что имя пользователя не занято и пароли совпадают.

    Поля:
        username (StringField): Поле ввода имени пользователя с валидаторами для обязательного ввода и длины (4-100 символов).
        password (PasswordField): Поле ввода пароля с валидаторами для обязательного ввода и длины (8-80 символов).
        confirm_password (PasswordField): Поле ввода подтверждения пароля с валидаторами для соответствия паролю.
        submit (SubmitField): Кнопка отправки формы.

    Методы:
        validate_username(username): Проверяет, что имя пользователя не занято.
            Аргументы:
                username: Поле ввода имени пользователя для проверки.
            Генерирует исключение:
                ValidationError: Если имя пользователя уже занято.
    """

    username = StringField(
        "Username", validators=[InputRequired(), Length(min=4, max=100)]
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=80)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is already taken.")


class LoginForm(FlaskForm):
    """
    Форма входа пользователей на Flask.

    Поля:
        username (StringField): Поле ввода имени пользователя с валидаторами для обязательного ввода и длины (4-100 символов).
        password (PasswordField): Поле ввода пароля с валидаторами для обязательного ввода и длины (8-80 символов).
        submit (SubmitField): Кнопка отправки формы.
    """

    username = StringField(
        "Username", validators=[InputRequired(), Length(min=4, max=100)]
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=80)]
    )
    submit = SubmitField("Login")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Обрабатывает регистрацию новых пользователей.

    - GET: Отображает страницу регистрации с формой.
    - POST: Проверяет данные формы, хэширует пароль и сохраняет нового пользователя в базу данных.

    Возвращает:
        render_template: Страницу с формой регистрации или перенаправление на страницу входа после успешной регистрации.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully!", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Обрабатывает вход существующих пользователей.

    - GET: Отображает страницу входа с формой.
    - POST: Проверяет данные формы и аутентифицирует пользователя.

    Возвращает:
        render_template: Страницу с формой входа или перенаправление на панель управления после успешного входа.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session["user_id"] = user.id
            flash("Logged in successfully!", "success")
            return redirect(url_for("smm.dashboard"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
def logout():
    """
    Выход из системы.

    Удаляет идентификатор пользователя из сессии и перенаправляет на страницу входа.

    Возвращает:
        redirect: На страницу входа после выхода.
    """
    session.pop("user_id", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))
