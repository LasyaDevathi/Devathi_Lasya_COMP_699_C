from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class ReviewForm(FlaskForm):
    """Form for submitting package reviews."""
    rating = SelectField('Rating', choices=[
        ('5', '★★★★★ Excellent'),
        ('4', '★★★★☆ Very Good'),
        ('3', '★★★☆☆ Good'),
        ('2', '★★☆☆☆ Fair'),
        ('1', '★☆☆☆☆ Poor')
    ], validators=[DataRequired()])
    
    comment = TextAreaField('Your Review', validators=[
        DataRequired(),
        Length(min=10, max=500, message="Review must be between 10 and 500 characters.")
    ])
    
    submit = SubmitField('Submit Review')