import pytest
from flask_testing import TestCase
from api import app, db
from api.models import User

class BaseTestCase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        user = User(username='testuser', password_hash='testpass')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestUserAPI(BaseTestCase):
    def test_user_registration(self):
        """
        Test registering a new user.
        """
        with self.client:
            response = self.client.post('/users/register', json={
                'username': 'newuser',
                'password': 'newpass'
            })
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'User registered successfully', response.data)

    def test_login(self):
        """
        Test the login functionality.
        """
        with self.client:
            response = self.client.post('/login', data=dict(
                username='testuser',
                password='testpass'
            ), follow_redirects=True)
            self.assertIn(b'You were successfully logged in', response.data)

if __name__ == '__main__':
    pytest.main()
