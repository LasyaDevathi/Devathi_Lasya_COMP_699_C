from flask import render_template, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.main import main
from app.models import Notification

@main.route('/notifications')
@login_required
def notifications():
    """Display all notifications for the current user."""
    unread_notifications = Notification.query.filter_by(
        user_id=current_user.id, 
        is_read=False
    ).order_by(Notification.created_at.desc()).all()
    
    read_notifications = Notification.query.filter_by(
        user_id=current_user.id, 
        is_read=True
    ).order_by(Notification.created_at.desc()).limit(20).all()
    
    return render_template('notifications.html',
                          title='My Notifications',
                          unread_notifications=unread_notifications,
                          read_notifications=read_notifications)


@main.route('/notifications/<int:notification_id>/mark-read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """Mark a notification as read."""
    notification = Notification.query.get_or_404(notification_id)
    
    # Ensure the notification belongs to the current user
    if notification.user_id != current_user.id:
        flash('Access denied. This notification does not belong to your account.', 'danger')
        return redirect(url_for('main.notifications'))
    
    notification.is_read = True
    db.session.commit()
    
    # Check if this is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'notification_id': notification_id})
    
    flash('Notification marked as read.', 'success')
    return redirect(url_for('main.notifications'))


@main.route('/notifications/mark-all-read', methods=['POST'])
@login_required
def mark_all_notifications_read():
    """Mark all notifications as read."""
    unread_notifications = Notification.query.filter_by(
        user_id=current_user.id, 
        is_read=False
    ).all()
    
    for notification in unread_notifications:
        notification.is_read = True
    
    db.session.commit()
    
    # Check if this is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'count': len(unread_notifications)})
    
    flash('All notifications marked as read.', 'success')
    return redirect(url_for('main.notifications'))


@main.route('/notifications/<int:notification_id>/delete', methods=['POST'])
@login_required
def delete_notification(notification_id):
    """Delete a notification."""
    notification = Notification.query.get_or_404(notification_id)
    
    # Ensure the notification belongs to the current user
    if notification.user_id != current_user.id:
        flash('Access denied. This notification does not belong to your account.', 'danger')
        return redirect(url_for('main.notifications'))
    
    db.session.delete(notification)
    db.session.commit()
    
    # Check if this is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'notification_id': notification_id})
    
    flash('Notification deleted.', 'success')
    return redirect(url_for('main.notifications'))


# Import request for checking AJAX calls
from flask import request