from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.travel import travel
from app.travel.forms import ReviewForm
from app.models import TravelPackage, Booking, Review

@travel.route('/package/<int:package_id>/review', methods=['GET', 'POST'])
@login_required
def submit_review(package_id):
    """Handle review submission for a package."""
    package = TravelPackage.query.get_or_404(package_id)
    
    # Check if user has booked this package
    booking = Booking.query.filter_by(
        user_id=current_user.id,
        package_id=package_id,
        status='COMPLETED'  # Only allow reviews for completed bookings
    ).first()
    
    if not booking:
        flash('You can only review packages you have booked and completed.', 'warning')
        return redirect(url_for('travel.package_detail', package_id=package_id))
    
    # Check if user has already submitted a review for this package
    existing_review = Review.query.filter_by(
        user_id=current_user.id,
        package_id=package_id
    ).first()
    
    if existing_review:
        flash('You have already submitted a review for this package.', 'info')
        return redirect(url_for('travel.package_detail', package_id=package_id))
    
    form = ReviewForm()
    
    if form.validate_on_submit():
        review = Review(
            user_id=current_user.id,
            package_id=package_id,
            rating=int(form.rating.data),
            comment=form.comment.data
        )
        
        db.session.add(review)
        db.session.commit()
        
        flash('Your review has been submitted successfully!', 'success')
        return redirect(url_for('travel.package_detail', package_id=package_id))
    
    return render_template('travel/submit_review.html', 
                         title='Submit Review', 
                         form=form, 
                         package=package)


@travel.route('/review/<int:review_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    """Handle editing of a review."""
    review = Review.query.get_or_404(review_id)
    
    # Check if the review belongs to the current user
    if review.user_id != current_user.id:
        abort(403)  # Forbidden
    
    form = ReviewForm()
    
    # Pre-populate form with existing review data
    if request.method == 'GET':
        form.rating.data = str(review.rating)
        form.comment.data = review.comment
    
    if form.validate_on_submit():
        review.rating = int(form.rating.data)
        review.comment = form.comment.data
        
        db.session.commit()
        
        flash('Your review has been updated successfully!', 'success')
        return redirect(url_for('travel.package_detail', package_id=review.package_id))
    
    return render_template('travel/submit_review.html', 
                          title='Edit Review', 
                          form=form, 
                          package=review.travel_package,
                          is_edit=True)


@travel.route('/review/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    """Handle deletion of a review."""
    review = Review.query.get_or_404(review_id)
    
    # Check if the review belongs to the current user
    if review.user_id != current_user.id:
        abort(403)  # Forbidden
    
    package_id = review.package_id
    
    db.session.delete(review)
    db.session.commit()
    
    flash('Your review has been deleted.', 'info')
    return redirect(url_for('travel.package_detail', package_id=package_id))