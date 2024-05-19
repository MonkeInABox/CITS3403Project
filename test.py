#!/usr/bin/env python
import unittest
from app import create_app, db, current_app
from app.models import User, Post, Comment
from config import Config
from app.posts.forms import PostNewPost
#from selenium import webdriver, multiprocessing
#from selenium.webdriver.chrome.service import Service as ChromeService
#from webdriver_manager.chrome import ChromeDriverManager


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = 'test'
    RECAPTCHA_PRIVATE_KEY = 'test'
    RECAPTCHA_OPTIONS = {'theme': 'white'}


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        with self.app_context:
            db.create_all()

    def test_password_hashing(self):
        u = User(username='susan', email='susan@example.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))
    
    def test_post(self):
        post_data = {
            'body': "I love Harrison Ford, what's a good movie with him in it?",
            'category': 'film',
            'submit': 'Submit Post'
        }
        current_user = User(id = 1, username = "test", email = "ford@gmail.com")
        result = self.app.post('/newpost', data = post_data, current_user=current_user)
        with self.app_context:
            post = Post.query.filter_by(category='film').first()
            self.assertEqual(post.body == "I love Harrison Ford, what's a good movie with him in it?")


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

localHost = "http://localhost:5000"

#class SeleniumTests(unittest.TestCase):
#    def setUp(self):
#        self.app = create_app(TestConfig)
#        self.app_context = self.app.app_context()
#        self.app_context.push()
#        db.create_all()

#        self.server_thread = multiprocessing.Process(target=self.testApp.run)
#        self.server_thread.start()

#        self.driver = webdriver.Chrome()
#        self.driver.get(localHost)

#    def tearDown(self):
#        self.server_thread.terminate()
#        self.driver.close()
#        db.session.remove()
#        db.drop_all()
#        self.app_context.pop()
    


        
if __name__ == '__main__':
    unittest.main(verbosity=2)