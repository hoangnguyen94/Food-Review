from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length


class CreateUserForm(FlaskForm):
    """form to create a users."""

    username = StringField('Username', 
        validators=[DataRequired()])
    password = PasswordField('Password', 
        validators=[DataRequired(), Length(min=6)])
    email = StringField('E-mail',
        validators=[DataRequired(), Email()])
    firstname = StringField('First Name',
        validators=[DataRequired()])
    lastname = StringField('Last Name',
        validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', 
        validators=[DataRequired()])
    password = PasswordField('Password', 
        validators=[Length(min=6)])

class FoodSearchForm(FlaskForm):
    "form to search for food."

    food = StringField('Name',
        validators=[DataRequired()])
    quantity = IntegerField('Quantity',
        validators=[DataRequired()])