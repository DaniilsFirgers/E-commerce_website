from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.models import User
from flask_wtf.file import FileField, FileAllowed
from wtforms.widgets import TextArea

CITIES=[
    'Daugavpils',
    'Jekabpils',
    'Jelgava',
    'Jūrmala',
    'Liepāja',
    'Rēzekne',
    'Rīga',
    'Valmiera',
    'Ventspils',
    'Other city'
]

CATEGORIES=[
    "Cell Phones",
    "Computers",
    "Tablets",
    "TV&Video",
    "Photo Cameras",
    "E-Books",
]

class UserRegistration(FlaskForm):
    username = StringField('Username: *', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email: *', validators=[DataRequired(), Email()])
    city = SelectField('Address: *', choices=CITIES, validators=[DataRequired()])
    phone_number = StringField('Phone Number: *', validators=[DataRequired(), Length(min=8, max=8)])
    password = PasswordField('Password: *', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password: *', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        username_taken = User.query.filter_by(username=username.data).first()
        if username_taken:
            raise ValidationError("This Username is taken. Please choose a different one!")

    def validate_email(self, email):
        email_taken = User.query.filter_by(email=email.data).first()
        if email_taken:
            raise ValidationError("This Email is already taken. Please choose a different one!")
    
    def validate_phone_number(self, phone_number):
        phone_number_taken = User.query.filter_by(phone_number=phone_number.data).first()
        if phone_number_taken:
            raise ValidationError("This Phone Number is already taken. Please choose a different one!")

class LoginUser(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Sign In')


class NewAd(FlaskForm):
    brand = StringField("Brand and model: *", validators=[DataRequired()])
    category = SelectField("Category: *", choices=CATEGORIES, validators=[DataRequired()])
    price = StringField("Price: *", validators=[DataRequired()])
    condition = SelectField("Condition: *", choices=["New", "Pre-owned"], validators=[DataRequired()])
    characteristics = StringField("Characteristics: *", validators=[Length(max=500)])
    description = TextAreaField("Description: ", validators=[Length(max=200)], widget=TextArea())
    image = FileField("Product Image: ", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Submit')


class Search(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")