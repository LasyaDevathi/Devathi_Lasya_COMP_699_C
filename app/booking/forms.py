from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from datetime import datetime, timedelta


class BookingForm(FlaskForm):
    """Form for creating a new booking."""
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[DataRequired()], format='%Y-%m-%d')
    num_guests = IntegerField('Number of Guests', validators=[DataRequired(), NumberRange(min=1)])
    special_requests = TextAreaField('Special Requests')
    submit = SubmitField('Book Now')
    
    def validate_start_date(self, start_date):
        """Validate that start date is not in the past."""
        if start_date.data < datetime.now().date():
            raise ValidationError('Start date cannot be in the past.')
    
    def validate_end_date(self, end_date):
        """Validate that end date is after start date."""
        if 'start_date' in self.data and end_date.data <= self.start_date.data:
            raise ValidationError('End date must be after start date.')
        
        # Optional: enforce maximum booking duration
        if 'start_date' in self.data:
            max_duration = 30  # Maximum booking duration in days
            duration = (end_date.data - self.start_date.data).days
            if duration > max_duration:
                raise ValidationError(f'Maximum booking duration is {max_duration} days.')


class PaymentForm(FlaskForm):
    """Form for processing payment."""
    card_holder = StringField('Card Holder Name', validators=[DataRequired()])
    card_number = StringField('Card Number', validators=[DataRequired()])
    expiry_month = StringField('Expiry Month (MM)', validators=[DataRequired()])
    expiry_year = StringField('Expiry Year (YYYY)', validators=[DataRequired()])
    cvv = StringField('CVV', validators=[DataRequired()])
    submit = SubmitField('Complete Payment')