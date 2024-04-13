from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator
import games.authentication.services as services
import games.adapters.repository as repo


authentication_blueprint = Blueprint('auth_bp', __name__, url_prefix='/authentication')


# Register view function
@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_test = None
    if form.validate_on_submit():
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)
            return redirect(url_for('auth_bp.login'))
        except services.NameNotUniqueException:
            user_name_test = "This username is already in use ;w;  Please try different username!"
    return render_template("authentication/auth.html",
                           title = 'Register',
                           form = form,
                           user_name_error_message = user_name_test,
                           handler_url = url_for('auth_bp.register')
                           )


# Login view function
@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name_not_recognised = None
    password_does_not_match_user_name = None

    if form.validate_on_submit():
        try:
            user = services.get_user(form.user_name.data, repo.repo_instance)

            # Authenticate user.
            services.authenticate_user(user['username'], form.password.data, repo.repo_instance)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['username'] = user['username']
            print("Login successful")
            return redirect(url_for('home_bp.home'))

        except services.UnknownUserException:
            user_name_not_recognised = 'We can not find the username you entered, please enter the correct username!'

        except services.AuthenticationException:
            # Authentication failed, set a suitable error message.
            password_does_not_match_user_name = 'Incorrect Password, Please check username and password again!'

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'authentication/auth.html',
        title='Login',
        user_name_error_message=user_name_not_recognised,
        password_error_message=password_does_not_match_user_name,
        form=form,
        handler_url=url_for('auth_bp.login')
    )


# Logout view function
@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


@authentication_blueprint.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('auth_bp.login'))
    form = ChangePasswordForm()
    password_wrong = None
    different_password = None
    username = session['username']

    if form.validate_on_submit():
        try:
            user = services.get_user(username, repo.repo_instance)

            # Authenticate user
            services.authenticate_user(username, form.old_password.data, repo.repo_instance)
            print("Succesfully authenticated")
            services.change_password(username, form.new_password1.data, form.new_password2.data, repo.repo_instance)
            print("Succesfully changed password")
            return redirect(url_for('profile_bp.profile'))

        except services.AuthenticationException:
            # Authentication failed, set a suitable error message.
            password_wrong = 'Incorrect current Password, Please check the password again!'

        except services.DifferentPasswordException:
            # User typed different password, set a suitable error message.
            different_password = 'Two passwords are different, please check new passwords again!'

    return render_template(
        'authentication/changePassword.html',
        title='Changing Password',
        wrong_password_error_message=password_wrong,
        different_password_error_message=different_password,
        form=form,
        handler_url=url_for('auth_bp.change_password')
    )


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = 'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Please enter the username'),
        Length(min=3, message='Your username is too short, username must be at least 3 characters long')])
    password = PasswordField('Password', [
        DataRequired(message='Please enter the password'),
        PasswordValid()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Login')


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('auth_bp.login'))
        return view(**kwargs)
    return wrapped_view


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('OldPassword', [
        DataRequired()])
    new_password1 = PasswordField('NewPassword', [
        DataRequired(message='Please enter the password'),
        PasswordValid()])
    new_password2 = PasswordField('NewPassword2', [
        DataRequired(message='Please enter the password'),
        PasswordValid()])
    submit = SubmitField('Change')