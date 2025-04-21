import os
from app import create_app, db
from app.models import User, Role, TravelPackage, Booking, Review, Payment, Notification, Itinerary

app = create_app(os.getenv('FLASK_ENV') or 'default')

@app.shell_context_processor
def make_shell_context():
    """Add database instance and models to flask shell context."""
    return {
        'db': db, 
        'User': User, 
        'Role': Role,
        'TravelPackage': TravelPackage,
        'Booking': Booking,
        'Review': Review,
        'Payment': Payment,
        'Notification': Notification,
        'Itinerary': Itinerary
    }


if __name__ == '__main__':
    app.run(debug=True)