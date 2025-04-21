from app import create_app, db
from app.models import User, Role, TravelPackage, Itinerary
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def seed_database():
    """Add initial sample data to the database."""
    app = create_app('development')
    
    with app.app_context():
        # Create roles if they don't exist
        admin_role = Role.query.filter_by(name='Admin').first()
        if not admin_role:
            admin_role = Role(name='Admin')
            db.session.add(admin_role)

        traveler_role = Role.query.filter_by(name='Traveler').first()
        if not traveler_role:
            traveler_role = Role(name='Traveler')
            db.session.add(traveler_role)

        agent_role = Role.query.filter_by(name='Agent').first()
        if not agent_role:
            agent_role = Role(name='Agent')
            db.session.add(agent_role)
        
        db.session.commit()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                first_name='Admin',
                last_name='User',
                phone='+1234567890',
                address='123 Admin St, Admin City',
                role=admin_role
            )
            admin.password = 'adminpassword'
            db.session.add(admin)
        
        # Create sample traveler if it doesn't exist
        traveler = User.query.filter_by(email='user@example.com').first()
        if not traveler:
            traveler = User(
                username='traveler',
                email='user@example.com',
                first_name='John',
                last_name='Doe',
                phone='+9876543210',
                address='456 Traveler Ave, Travel City',
                role=traveler_role
            )
            traveler.password = 'userpassword'
            db.session.add(traveler)
        
        db.session.commit()
        
        # Create sample travel packages if none exist
        if TravelPackage.query.count() == 0:
            packages = [
                {
                    'name': 'Bali Paradise Getaway',
                    'description': 'Experience the beauty of Bali with this all-inclusive package. Visit ancient temples, relax on pristine beaches, and immerse yourself in the local culture. This package includes accommodation, daily breakfast, and guided tours to top attractions.',
                    'destination': 'Bali, Indonesia',
                    'duration_days': 7,
                    'price_per_day': 120.00,
                    'max_guests': 4,
                    'is_available': True,
                    'image_url': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4'
                },
                {
                    'name': 'Tokyo Explorer',
                    'description': 'Discover the fascinating blend of traditional and modern in Tokyo. Visit ancient shrines, explore bustling markets, and experience the vibrant nightlife. This package includes hotel accommodation, city transport pass, and guided tours.',
                    'destination': 'Tokyo, Japan',
                    'duration_days': 5,
                    'price_per_day': 180.00,
                    'max_guests': 2,
                    'is_available': True,
                    'image_url': 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf'
                },
                {
                    'name': 'Paris Romance',
                    'description': 'Experience the city of love with this romantic Paris getaway. Enjoy stunning views from the Eiffel Tower, visit world-class museums, and stroll along the Seine. Package includes boutique hotel accommodation and skip-the-line tickets to major attractions.',
                    'destination': 'Paris, France',
                    'duration_days': 4,
                    'price_per_day': 220.00,
                    'max_guests': 2,
                    'is_available': True,
                    'image_url': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34'
                },
                {
                    'name': 'African Safari Adventure',
                    'description': 'Embark on an unforgettable wildlife safari in Kenya. Witness the majestic Big Five in their natural habitat and experience authentic local culture. Package includes lodge accommodation, game drives, and meals.',
                    'destination': 'Nairobi, Kenya',
                    'duration_days': 6,
                    'price_per_day': 250.00,
                    'max_guests': 6,
                    'is_available': True,
                    'image_url': 'https://images.unsplash.com/photo-1523805009345-7448845a9e53'
                },
                {
                    'name': 'New York City Break',
                    'description': 'Take a bite out of the Big Apple with this exciting city break. Explore iconic landmarks, enjoy Broadway shows, and shop in world-famous stores. Package includes central hotel accommodation and a city attraction pass.',
                    'destination': 'New York, USA',
                    'duration_days': 3,
                    'price_per_day': 200.00,
                    'max_guests': 4,
                    'is_available': True,
                    'image_url': 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9'
                },
                {
                    'name': 'Greek Islands Cruise',
                    'description': 'Sail through the stunning Greek islands on this luxury cruise package. Visit Santorini, Mykonos, and other beautiful islands. Package includes cabin accommodation, all meals, and shore excursions.',
                    'destination': 'Athens, Greece',
                    'duration_days': 8,
                    'price_per_day': 280.00,
                    'max_guests': 2,
                    'is_available': True,
                    'image_url': 'https://images.unsplash.com/photo-1515861461225-1488dfdaf2d8'
                }
            ]
            
            # Add packages to the database
            for package_data in packages:
                package = TravelPackage(**package_data)
                db.session.add(package)
            
            db.session.commit()
            
            # Add itineraries for the first package
            bali_package = TravelPackage.query.filter_by(name='Bali Paradise Getaway').first()
            if bali_package:
                itinerary_items = [
                    {
                        'package_id': bali_package.id,
                        'day_number': 1,
                        'title': 'Arrival and Welcome Dinner',
                        'description': 'Arrive at Denpasar Airport, transfer to your hotel in Ubud. Evening welcome dinner with traditional Balinese performances.',
                        'location': 'Ubud, Bali'
                    },
                    {
                        'package_id': bali_package.id,
                        'day_number': 2,
                        'title': 'Sacred Temples Tour',
                        'description': 'Visit the sacred Tirta Empul Temple and participate in a traditional purification ceremony. Afternoon exploration of Goa Gajah (Elephant Cave).',
                        'location': 'Ubud, Bali'
                    },
                    {
                        'package_id': bali_package.id,
                        'day_number': 3,
                        'title': 'Rice Terraces and Art Villages',
                        'description': 'Morning visit to the stunning Tegallalang Rice Terraces. Afternoon tour of Ubud\'s famous art villages and craft centers.',
                        'location': 'Ubud, Bali'
                    },
                    {
                        'package_id': bali_package.id,
                        'day_number': 4,
                        'title': 'Transfer to Beachside Resort',
                        'description': 'Morning yoga session, then transfer to your luxury beachside resort in Nusa Dua. Free afternoon to enjoy the beach.',
                        'location': 'Nusa Dua, Bali'
                    },
                    {
                        'package_id': bali_package.id,
                        'day_number': 5,
                        'title': 'Uluwatu Temple and Kecak Dance',
                        'description': 'Day at leisure. Evening visit to the clifftop Uluwatu Temple followed by traditional Kecak fire dance performance at sunset.',
                        'location': 'Uluwatu, Bali'
                    },
                    {
                        'package_id': bali_package.id,
                        'day_number': 6,
                        'title': 'Water Sports and Spa',
                        'description': 'Morning water sports activities including snorkeling. Afternoon Balinese spa treatment.',
                        'location': 'Nusa Dua, Bali'
                    },
                    {
                        'package_id': bali_package.id,
                        'day_number': 7,
                        'title': 'Departure',
                        'description': 'Free time for last-minute shopping or relaxation. Transfer to Denpasar Airport for departure.',
                        'location': 'Denpasar, Bali'
                    }
                ]
                
                for item_data in itinerary_items:
                    itinerary = Itinerary(**item_data)
                    db.session.add(itinerary)
                
                db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()