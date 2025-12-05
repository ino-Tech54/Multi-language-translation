from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
import re
from models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Invalid email address")
    ])
    
    name = StringField('Name', validators=[
        DataRequired(message="Name is required"),
        Length(min=4, max=50, message="Name must be between 4–50 characters"),
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, message="Password must be at least 8 characters"),
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message="Passwords must match")
    ])
    
    role = SelectField('Role', choices=[
        ('Analyst', 'Analyst'),
       # ('Customer', 'Customer')
    ], validators=[DataRequired(message="Role is required")])
    
    submit = SubmitField('Register')

    def validate_email(self, field):
        """Ensure email format is valid, unique, and matches role requirements"""
        email = field.data.lower()

        # Basic email format check
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError("Invalid email address format")
        
        # Check uniqueness
        if User.query.filter_by(email=email).first():
            raise ValidationError("Email already registered")

        # Role-specific rule
        if self.role.data == 'Farmer' and 'bs' not in email:
            raise ValidationError("Email must contain 'bs'")

    def validate_name(self, field):
        """Ensure name format is valid and unique"""
        name = field.data.strip()
        
        if not re.match(r'^[a-zA-Z0-9_ ]+$', name):
            raise ValidationError("Name can only contain letters, numbers, spaces and underscores")
        
        if User.query.filter_by(name=name).first():
            raise ValidationError("Name already taken")

    def validate_password(self, field):
        """Ensure password is strong"""
        password = field.data
        
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            raise ValidationError(
                "Password must contain at least 8 characters, one uppercase, one lowercase, and one number"
            )


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Invalid email address")
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_email(self, field):
        """Ensure the email exists in the system"""
        email = field.data.lower()
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValidationError("Email not registered")
