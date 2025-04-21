from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.main import main
from app.models import TravelPackage, Booking


@main.route('/')
def index():
    """Render the homepage."""
    # Get featured travel packages (limit to 6)
    featured_packages = TravelPackage.query.filter_by(is_available=True).limit(6).all()
    
    return render_template('index.html', 
                          title='Home',
                          featured_packages=featured_packages)


@main.route('/dashboard')
@login_required
def dashboard():
    """Render the user dashboard."""
    # Get user's recent bookings
    recent_bookings = Booking.query.filter_by(user_id=current_user.id)\
                                  .order_by(Booking.created_at.desc())\
                                  .limit(5)\
                                  .all()
    
    # Get user's upcoming trips (bookings with future start dates and confirmed status)
    upcoming_trips = Booking.query.filter_by(user_id=current_user.id, status='CONFIRMED')\
                               .filter(Booking.start_date >= datetime.now().date())\
                               .order_by(Booking.start_date)\
                               .limit(3)\
                               .all()
    
    # Get recommended packages based on user's past bookings
    # This is a simple implementation; in a real app, this could be more sophisticated
    recommended_packages = TravelPackage.query.filter_by(is_available=True)\
                                            .limit(4)\
                                            .all()
    
    return render_template('dashboard.html',
                          title='Dashboard',
                          recent_bookings=recent_bookings,
                          upcoming_trips=upcoming_trips,
                          recommended_packages=recommended_packages)


@main.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html', title='About Us')


@main.route('/contact')
def contact():
    """Render the contact page."""
    return render_template('contact.html', title='Contact Us')


@main.route('/search')
def search():
    """Handle global search and redirect to appropriate search results."""
    query = request.args.get('query', '')
    destination = request.args.get('destination', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    guests = request.args.get('guests', 1, type=int)
    
    # Redirect to the travel search with the query parameters
    return redirect(url_for('travel.search_packages',
                           destination=destination,
                           start_date=start_date,
                           end_date=end_date,
                           guests=guests,
                           query=query))


# Import datetime for upcoming_trips query
from datetime import datetime