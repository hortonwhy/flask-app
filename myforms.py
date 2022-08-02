""" WTForms module, containing forms for user interaction"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    """ Login Form: Email, password """

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=30)])


class RegisterForm(FlaskForm):
    """Registration Form fname, lname, email, password """

    fname = StringField("First Name", validators=[DataRequired(), Length(max=30)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(max=30)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            EqualTo("confirm", message="Passwords must match"),
            Length(max=30),
        ],
    )
    confirm = PasswordField("Repeat Password")


class PostForm(FlaskForm):
    """ Blog post form, title and body """

    title = StringField("Title", validators=[DataRequired(), Length(max=30)])
    body = TextAreaField("Body", validators=[DataRequired(), Length(max=300)])
