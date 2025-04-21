from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

class ProfileForm(FlaskForm):
    """Form for editing user profile information."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=64)])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    address = TextAreaField('Address', validators=[Length(max=256)])
    
    # Optional password change fields
    password = PasswordField('New Password', validators=[Optional(), Length(min=8)])
    password2 = PasswordField('Confirm New Password', validators=[
        EqualTo('password', message='Passwords must match.')
    ])
    
    submit = SubmitField('Update Profile')