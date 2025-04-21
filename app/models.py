from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class Role(db.Model):
    """User role model."""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return f'<Role {self.name}>'


class User(UserMixin, db.Model):
    """User model."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(256))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy='dynamic')
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    
    @property
    def password(self):
        """Prevent password from being accessed."""
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """Verify password against stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class TravelPackage(db.Model):
    """Travel package model."""
    __tablename__ = 'travel_packages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    destination = db.Column(db.String(128), nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)
    max_guests = db.Column(db.Integer, default=10)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(256))
    
    # Relationships
    bookings = db.relationship('Booking', backref='travel_package', lazy='dynamic')
    reviews = db.relationship('Review', backref='travel_package', lazy='dynamic')
    itineraries = db.relationship('Itinerary', backref='travel_package', lazy='dynamic')
    
    def __repr__(self):
        return f'<TravelPackage {self.name}>'


class Booking(db.Model):
    """Booking model."""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('travel_packages.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    num_guests = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='PENDING_PAYMENT')  # PENDING_PAYMENT, CONFIRMED, CANCELLED, COMPLETED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    payments = db.relationship('Payment', backref='booking', lazy='dynamic')
    
    def __repr__(self):
        return f'<Booking {self.id}>'


class Review(db.Model):
    """Review model."""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('travel_packages.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.id}>'


class Payment(db.Model):
    """Payment model."""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(20), nullable=False)  # CREDIT_CARD, PAYPAL, BANK_TRANSFER
    status = db.Column(db.String(20), default='PENDING')  # PENDING, COMPLETED, FAILED, REFUNDED
    transaction_id = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Payment {self.id}>'


class Notification(db.Model):
    """Notification model."""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20))  # BOOKING_CONFIRMATION, PAYMENT_CONFIRMATION, BOOKING_REMINDER, etc.
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Notification {self.id}>'


class Itinerary(db.Model):
    """Itinerary model for travel packages."""
    __tablename__ = 'itineraries'
    
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('travel_packages.id'), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(128))
    
    def __repr__(self):
        return f'<Itinerary Day {self.day_number} for Package {self.package_id}>'


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """User loader function for Flask-Login."""
    return User.query.get(int(user_id))