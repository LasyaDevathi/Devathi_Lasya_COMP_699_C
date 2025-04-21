from flask import render_template, redirect, url_for, flash, request, jsonify
from app.travel import travel
from app.models import TravelPackage, Itinerary, Review
from sqlalchemy import or_


@travel.route('/packages')
def packages():
    """Display all available travel packages."""
    page = request.args.get('page', 1, type=int)
    packages = TravelPackage.query.filter_by(is_available=True)\
                               .order_by(TravelPackage.created_at.desc())\
                               .paginate(page=page, per_page=9)
    
    return render_template('travel/packages.html', 
                          title='Travel Packages',
                          packages=packages)


@travel.route('/search')
def search_packages():
    """Search for travel packages based on criteria."""
    # Get search parameters
    destination = request.args.get('destination', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    guests = request.args.get('guests', 1, type=int)
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    
    # Build query
    package_query = TravelPackage.query.filter_by(is_available=True)
    
    # Apply filters if provided
    if destination:
        package_query = package_query.filter(TravelPackage.destination.ilike(f'%{destination}%'))
    
    if query:
        package_query = package_query.filter(
            or_(
                TravelPackage.name.ilike(f'%{query}%'),
                TravelPackage.description.ilike(f'%{query}%'),
                TravelPackage.destination.ilike(f'%{query}%')
            )
        )
    
    if guests:
        package_query = package_query.filter(TravelPackage.max_guests >= guests)
    
    # Order and paginate results
    packages = package_query.order_by(TravelPackage.created_at.desc())\
                          .paginate(page=page, per_page=9)
    
    return render_template('travel/search_results.html',
                          title='Search Results',
                          packages=packages,
                          search_params={
                              'destination': destination,
                              'start_date': start_date,
                              'end_date': end_date,
                              'guests': guests,
                              'query': query
                          })


@travel.route('/package/<int:package_id>')
def package_detail(package_id):
    """Display details for a specific travel package."""
    package = TravelPackage.query.get_or_404(package_id)
    
    # Get itinerary for the package
    itinerary = Itinerary.query.filter_by(package_id=package_id)\
                             .order_by(Itinerary.day_number).all()
    
    # Get reviews for the package
    reviews = Review.query.filter_by(package_id=package_id)\
                        .order_by(Review.created_at.desc()).all()
    
    # Calculate average rating
    avg_rating = 0
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    
    return render_template('travel/package_detail.html',
                          title=package.name,
                          package=package,
                          itinerary=itinerary,
                          reviews=reviews,
                          avg_rating=avg_rating)