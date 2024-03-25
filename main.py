from api import app, db
from api.models import User, Role, Device, MedicalRecord, Appointment, Alert, Message
import os

def setup_database(app):
    """
    Creates the database tables based on the models if they don't already exist.
    """
    with app.app_context():
        db.create_all()

def create_default_users():
    """
    Create some default users for testing purposes.
    """
    with app.app_context():
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', password_hash='adminpass')
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///health_monitoring_system.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a_secret_key_for_session_management')

    setup_database(app)
    create_default_users()

    app.run(debug=True, host='0.0.0.0', port=5000)
