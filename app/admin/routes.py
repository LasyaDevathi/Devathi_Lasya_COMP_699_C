from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.admin import admin
from app.models import User, TravelPackage, Booking, Review, Role, Itinerary


def admin_required(func):
    """Decorator to check if user has admin role."""
    @login_required
    def decorated_view(*args, **kwargs):
        if not current_user.role or current_user.role.name != 'Admin':
            abort(403)
        return func(*args, **kwargs)
    decorated_view.__name__ = func.__name__
    return decorated_view


@admin.route('/')
@admin_required
def index():
    """Admin dashboard."""
    # Get counts for dashboard stats
    user_count = User.query.count()
    package_count = TravelPackage.query.count()
    booking_count = Booking.query.count()
    review_count = Review.query.count()
    
    # Get recent bookings
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    
    return render_template('admin/index.html',
                          title='Admin Dashboard',
                          stats={
                              'users': user_count,
                              'packages': package_count,
                              'bookings': booking_count,
                              'reviews': review_count
                          },
                          recent_bookings=recent_bookings)


@admin.route('/users')
@admin_required
def users():
    """List all users."""
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=20)
    
    return render_template('admin/users.html',
                          title='User Management',
                          users=users)


@admin.route('/packages')
@admin_required
def packages():
    """List all travel packages."""
    page = request.args.get('page', 1, type=int)
    packages = TravelPackage.query.order_by(TravelPackage.created_at.desc()).paginate(page=page, per_page=10)
    
    return render_template('admin/packages.html',
                          title='Travel Packages',
                          packages=packages)


@admin.route('/package/new', methods=['GET', 'POST'])
@admin_required
def new_package():
    """Create a new travel package."""
    # In a real application, this would use a form to create the package
    # For now, this is a simplified implementation
    if request.method == 'POST':
        # Create new package from form data
        package = TravelPackage(
            name=request.form.get('name'),
            description=request.form.get('description'),
            destination=request.form.get('destination'),
            duration_days=int(request.form.get('duration_days')),
            price_per_day=float(request.form.get('price_per_day')),
            max_guests=int(request.form.get('max_guests')),
            is_available=bool(request.form.get('is_available')),
            image_url=request.form.get('image_url')
        )
        
        db.session.add(package)
        db.session.commit()
        
        flash('Travel package created successfully!', 'success')
        return redirect(url_for('admin.packages'))
    
    return render_template('admin/package_form.html',
                          title='New Travel Package')


@admin.route('/package/edit/<int:package_id>', methods=['GET', 'POST'])
@admin_required
def edit_package(package_id):
    """Edit an existing travel package."""
    package = TravelPackage.query.get_or_404(package_id)
    
    # In a real application, this would use a form to edit the package
    # For now, this is a simplified implementation
    if request.method == 'POST':
        # Update package from form data
        package.name = request.form.get('name')
        package.description = request.form.get('description')
        package.destination = request.form.get('destination')
        package.duration_days = int(request.form.get('duration_days'))
        package.price_per_day = float(request.form.get('price_per_day'))
        package.max_guests = int(request.form.get('max_guests'))
        package.is_available = bool(request.form.get('is_available'))
        package.image_url = request.form.get('image_url')
        
        db.session.commit()
        
        flash('Travel package updated successfully!', 'success')
        return redirect(url_for('admin.packages'))
    
    return render_template('admin/package_form.html',
                          title='Edit Travel Package',
                          package=package)


@admin.route('/bookings')
@admin_required
def bookings():
    """List all bookings."""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', None)
    
    # Build query with optional status filter
    query = Booking.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    # Get paginated bookings ordered by creation date (newest first)
    bookings = query.order_by(Booking.created_at.desc()).paginate(page=page, per_page=20)
    
    return render_template('admin/bookings.html',
                          title='Booking Management',
                          bookings=bookings,
                          status_filter=status_filter)


@admin.route('/booking/<int:booking_id>')
@admin_required
def booking_detail(booking_id):
    """View booking details."""
    booking = Booking.query.get_or_404(booking_id)
    user = User.query.get(booking.user_id)
    package = TravelPackage.query.get(booking.package_id)
    
    return render_template('admin/booking_detail.html',
                          title='Booking Details',
                          booking=booking,
                          user=user,
                          package=package)


@admin.route('/booking/update/<int:booking_id>', methods=['POST'])
@admin_required
def update_booking(booking_id):
    """Update booking status."""
    booking = Booking.query.get_or_404(booking_id)
    
    # Update status from form data
    new_status = request.form.get('status')
    if new_status in ['PENDING_PAYMENT', 'CONFIRMED', 'CANCELLED', 'COMPLETED']:
        booking.status = new_status
        db.session.commit()
        flash('Booking status updated successfully!', 'success')
    else:
        flash('Invalid booking status.', 'danger')
    
    return redirect(url_for('admin.booking_detail', booking_id=booking_id))


@admin.route('/reviews')
@admin_required
def reviews():
    """List all reviews."""
    page = request.args.get('page', 1, type=int)
    reviews = Review.query.order_by(Review.created_at.desc()).paginate(page=page, per_page=20)
    
    return render_template('admin/reviews.html',
                          title='Review Management',
                          reviews=reviews)