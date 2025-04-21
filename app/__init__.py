from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Register blueprints
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from app.travel import travel as travel_blueprint
    app.register_blueprint(travel_blueprint, url_prefix='/travel')
    
    from app.booking import booking as booking_blueprint
    app.register_blueprint(booking_blueprint, url_prefix='/booking')
    
    from app.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    """Register error handlers with the Flask application."""
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html'), 500

# Import render_template here to avoid circular imports
from flask import render_template