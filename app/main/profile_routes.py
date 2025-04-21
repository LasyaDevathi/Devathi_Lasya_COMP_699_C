from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.main import main
from app.main.forms import ProfileForm

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Handle user profile viewing and editing."""
    form = ProfileForm()
    
    # Pre-populate form with current user data
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.phone.data = current_user.phone
        form.address.data = current_user.address
    
    if form.validate_on_submit():
        # Update user data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        
        # Only update username and email if changed (and validate uniqueness)
        if form.username.data != current_user.username:
            # Check if username is already taken
            from app.models import User
            if User.query.filter_by(username=form.username.data).first():
                flash('Username already in use. Please choose a different one.', 'danger')
                return render_template('profile.html', title='Edit Profile', form=form)
            current_user.username = form.username.data
            
        if form.email.data != current_user.email:
            # Check if email is already taken
            from app.models import User
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already in use. Please choose a different one.', 'danger')
                return render_template('profile.html', title='Edit Profile', form=form)
            current_user.email = form.email.data
            
        # Update password if provided
        if form.password.data:
            current_user.password = form.password.data
            
        db.session.commit()
        flash('Your profile has been updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('profile.html', title='Edit Profile', form=form)