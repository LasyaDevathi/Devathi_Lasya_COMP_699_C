from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.booking import booking
from app.booking.forms import BookingForm, PaymentForm
from app.models import TravelPackage, Booking, Payment, Notification


@booking.route('/book/<int:package_id>', methods=['GET', 'POST'])
@login_required
def book_package(package_id):
    """Handle booking creation for a specific package."""
    package = TravelPackage.query.get_or_404(package_id)
    
    if not package.is_available:
        flash('Sorry, this package is currently not available for booking.', 'warning')
        return redirect(url_for('travel.package_detail', package_id=package_id))
    
    form = BookingForm()
    # Pre-fill form with data from URL parameters if available
    if request.method == 'GET':
        form.start_date.data = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d').date() \
            if request.args.get('start_date') else None
        form.end_date.data = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d').date() \
            if request.args.get('end_date') else None
        form.num_guests.data = int(request.args.get('guests', 1))
    
    if form.validate_on_submit():
        # Validate number of guests against package limit
        if form.num_guests.data > package.max_guests:
            flash(f'Maximum number of guests for this package is {package.max_guests}.', 'danger')
            return redirect(url_for('booking.book_package', package_id=package_id))
        
        # Calculate booking details
        start_date = form.start_date.data
        end_date = form.end_date.data
        num_guests = form.num_guests.data
        duration = (end_date - start_date).days
        total_price = package.price_per_day * duration * num_guests
        
        # Create the booking
        booking = Booking(
            user_id=current_user.id,
            package_id=package_id,
            start_date=start_date,
            end_date=end_date,
            num_guests=num_guests,
            total_price=total_price,
            status='PENDING_PAYMENT'
        )
        
        db.session.add(booking)
        db.session.commit()
        
        # Create notification
        notification = Notification(
            user_id=current_user.id,
            title='Booking Created',
            message=f'Your booking for {package.name} is pending payment.',
            type='BOOKING_CONFIRMATION'
        )
        db.session.add(notification)
        db.session.commit()
        
        flash('Booking created successfully! Please proceed to payment.', 'success')
        return redirect(url_for('booking.payment', booking_id=booking.id))
    
    return render_template('booking/booking_form.html',
                          title='Book Package',
                          form=form,
                          package=package)


@booking.route('/payment/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def payment(booking_id):
    """Handle payment for a booking."""
    booking_record = Booking.query.get_or_404(booking_id)
    
    # Ensure the booking belongs to the current user
    if booking_record.user_id != current_user.id:
        abort(403)
    
    # Ensure the booking is in PENDING_PAYMENT status
    if booking_record.status != 'PENDING_PAYMENT':
        flash('This booking is not pending payment.', 'warning')
        return redirect(url_for('booking.my_bookings'))
    
    package = TravelPackage.query.get(booking_record.package_id)
    form = PaymentForm()
    
    if form.validate_on_submit():
        # In a real application, process payment with a payment gateway
        # For this demonstration, we'll simulate a successful payment
        
        # Create payment record
        payment = Payment(
            booking_id=booking_id,
            amount=booking_record.total_price,
            method='CREDIT_CARD',
            status='COMPLETED',
            transaction_id=f'SIMULATED-{datetime.now().strftime("%Y%m%d%H%M%S")}'
        )
        
        # Update booking status
        booking_record.status = 'CONFIRMED'
        
        db.session.add(payment)
        db.session.commit()
        
        # Create confirmation notification
        notification = Notification(
            user_id=current_user.id,
            title='Payment Confirmed',
            message=f'Your payment of ${booking_record.total_price:.2f} for {package.name} has been received.',
            type='PAYMENT_CONFIRMATION'
        )
        db.session.add(notification)
        db.session.commit()
        
        flash('Payment processed successfully! Your booking is now confirmed.', 'success')
        return redirect(url_for('booking.booking_confirmation', booking_id=booking_id))
    
    return render_template('booking/payment_form.html',
                          title='Complete Payment',
                          form=form,
                          booking=booking_record,
                          package=package)


@booking.route('/confirmation/<int:booking_id>')
@login_required
def booking_confirmation(booking_id):
    """Display booking confirmation page."""
    booking_record = Booking.query.get_or_404(booking_id)
    
    # Ensure the booking belongs to the current user
    if booking_record.user_id != current_user.id:
        abort(403)
    
    package = TravelPackage.query.get(booking_record.package_id)
    payment = Payment.query.filter_by(booking_id=booking_id).first()
    
    return render_template('booking/confirmation.html',
                          title='Booking Confirmation',
                          booking=booking_record,
                          package=package,
                          payment=payment)


@booking.route('/my-bookings')
@login_required
def my_bookings():
    """Display user's bookings."""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', None)
    
    # Build query with optional status filter
    query = Booking.query.filter_by(user_id=current_user.id)
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    # Get paginated bookings ordered by creation date (newest first)
    bookings = query.order_by(Booking.created_at.desc())\
                   .paginate(page=page, per_page=10)
    
    return render_template('booking/my_bookings.html',
                          title='My Bookings',
                          bookings=bookings,
                          status_filter=status_filter)


@booking.route('/booking/<int:booking_id>')
@login_required
def booking_detail(booking_id):
    """Display details for a specific booking."""
    booking_record = Booking.query.get_or_404(booking_id)
    
    # Ensure the booking belongs to the current user
    if booking_record.user_id != current_user.id:
        abort(403)
    
    package = TravelPackage.query.get(booking_record.package_id)
    payment = Payment.query.filter_by(booking_id=booking_id).first()
    
    return render_template('booking/booking_detail.html',
                          title='Booking Details',
                          booking=booking_record,
                          package=package,
                          payment=payment)


@booking.route('/cancel/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    """Cancel a booking."""
    booking_record = Booking.query.get_or_404(booking_id)
    
    # Ensure the booking belongs to the current user
    if booking_record.user_id != current_user.id:
        abort(403)
    
    # Check if booking can be cancelled (e.g., not in the past, not already cancelled)
    if booking_record.start_date <= datetime.now().date():
        flash('Cannot cancel bookings that have already started or completed.', 'danger')
        return redirect(url_for('booking.booking_detail', booking_id=booking_id))
    
    if booking_record.status == 'CANCELLED':
        flash('This booking has already been cancelled.', 'warning')
        return redirect(url_for('booking.booking_detail', booking_id=booking_id))
    
    # Update booking status
    old_status = booking_record.status
    booking_record.status = 'CANCELLED'
    db.session.commit()
    
    # Create cancellation notification
    notification = Notification(
        user_id=current_user.id,
        title='Booking Cancelled',
        message=f'Your booking #{booking_id} has been cancelled.',
        type='BOOKING_CANCELLATION'
    )
    db.session.add(notification)
    db.session.commit()
    
    # In a real application, handle refunds if applicable
    if old_status == 'CONFIRMED':
        flash('Your booking has been cancelled. Refund process will be initiated.', 'info')
    else:
        flash('Your booking has been cancelled.', 'info')
    
    return redirect(url_for('booking.my_bookings'))