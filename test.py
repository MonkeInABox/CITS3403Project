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
        self.client = self.app.test_client()

        with self.app_context:
            self.current_user = User(id=1, username="test", email="test@example.com")
            self.current_user.set_password('test')  # Set a password if needed
            db.session.add(self.current_user)
            db.session.commit()

            # Log in the user
            with self.client.session_transaction() as session:
                session['_user_id'] = str(self.current_user.id)

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
                'category': 'film'
            }
            
            # Make the POST request to create a new post
            result = self.client.post('/newpost', data=post_data)

            # Check that the POST request was successful (redirect status code 302)
            self.assertEqual(result.status_code, 302)

            # Verify the post has been created in the database
            with self.app_context:
                post = db.session.query(Post).filter_by(category='film').first()
                self.assertIsNotNone(post)
                self.assertEqual(post.body, "I love Harrison Ford, what's a good movie with him in it?")
                self.assertEqual(post.user_id, self.current_user.id)

    def test_comment(self):
        with self.app_context:
            post = Post(body="What's a good movie with Harrison Ford?", category='film', user_id=self.current_user.id)
            db.session.add(post)
            db.session.commit()

        comment_data = {
            'body': "I also love Harrison Ford!"
        }

        result = self.client.post(f'/submit_comment/{post.id}', data=comment_data)

        self.assertEqual(result.status_code, 200)

        with self.app_context:
            comment = db.session.query(Comment).filter_by(post_id=post.id).first()
            self.assertIsNotNone(comment)
            self.assertEqual(comment.body, "I also love Harrison Ford!")
            self.assertEqual(comment.author_id, self.current_user.id)


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