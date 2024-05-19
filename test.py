#!/usr/bin/env python
import unittest
from flask import url_for
from app import create_app, db
from app.models import User,Post
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SERVER_NAME = 'localhost'  # Setting SERVER_NAME for URL building
    APPLICATION_ROOT = '/'     # Application root
    PREFERRED_URL_SCHEME = 'http'  # Preferred URL scheme
    WTF_CSRF_ENABLED = False  # Disable CSRF protection for testing



class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password')
        db.session.add(self.user)
        db.session.commit()
        if self._testMethodName not in ['test_user_registration']:
            self.login()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        response = self.client.post(url_for('auth.login'), data={
            'username': 'testuser',
            'password': 'password'
        }, follow_redirects=True)

    def test_password_hashing(self):
        u = User(username='testuser', email='testuser@example.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))
                                         
    def test_user_registration(self):
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password',
            'password2': 'password'
        },follow_redirects=True)
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user) 
        self.assertEqual(user.username, 'newuser')


        
if __name__ == '__main__':
    unittest.main(verbosity=2)