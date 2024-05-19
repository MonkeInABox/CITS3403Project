#!/usr/bin/env python
import unittest

from flask import url_for
import multiprocessing
from app import create_app, db
from flask import current_app
from app.models import User, Post, Comment, Like, Dislike
from config import Config
from app.posts.forms import PostNewPost
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SERVER_NAME = 'localhost'  # Setting SERVER_NAME for URL building
    APPLICATION_ROOT = '/'     # Application root
    PREFERRED_URL_SCHEME = 'http'  # Preferred URL scheme
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
         if self._testMethodName not in ['test_user_registration']:
            self.login()

            # Log in the user
            with self.client.session_transaction() as session:
                session['_user_id'] = str(self.current_user.id)

    def login(self):
        response = self.client.post(url_for('auth.login'), data={
            'username': 'testuser',
            'password': 'password'
        })

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
        })
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user) 
        self.assertEqual(user.username, 'newuser')

    def test_edit_profile(self):
        response = self.client.post('/edit_profile', data={
             'about_me': 'This is testing the about me.'
        })
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.about_me,'This is testing the about me.')   

    def test_logout(self):
        response = self.client.get(url_for('auth.logout'))
        response = self.client.get(url_for('main.profile', username='testuser'))
        self.assertIn(b'Login', response.data)

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

    def test_comment_filter(self):
        with self.app_context:
            post1 = Post(body="What's a good movie with Harrison Ford?", category='film', user_id=self.current_user.id)
            post2 = Post(body="What's a good song?", category='musc', user_id=self.current_user.id)
            post3 = Post(body="What's a good movie with Justin Bieber?", category='film', user_id=self.current_user.id)
            post4 = Post(body="What's a good movie with Harrison Ford?", category='film', user_id=self.current_user.id)
            post5 = Post(body="What's a good song?", category='musc', user_id=self.current_user.id)
            post6 = Post(body="What's a good movie with Justin Bieber?", category='film', user_id=self.current_user.id)
            post7 = Post(body="What's a good movie with Harrison Ford?", category='film', user_id=self.current_user.id)
            post8 = Post(body="What's a good song?", category='musc', user_id=self.current_user.id)
            post9 = Post(body="What's a good movie with Justin Bieber?", category='film', user_id=self.current_user.id)
            db.session.add(post1)
            db.session.commit()
            db.session.add(post2)
            db.session.commit()
            db.session.add(post3) # I need to commit after every one as the timestamps are needed
            db.session.commit()
            db.session.add(post4)
            db.session.commit()
            db.session.add(post5)
            db.session.commit()
            db.session.add(post6)
            db.session.commit()
            db.session.add(post7)
            db.session.commit()
            db.session.add(post8)
            db.session.commit()
            db.session.add(post9)
            db.session.commit()

            comment1 = Comment(body="Harrison test 1", author_id=self.current_user.id, post_id=post1.id)
            comment2 = Comment(body="Harrison test 2", author_id=self.current_user.id, post_id=post3.id)
            comment3 = Comment(body="Harrison test 3", author_id=self.current_user.id, post_id=post5.id)
            comment4 = Comment(body="Harrison test 4", author_id=self.current_user.id, post_id=post7.id)
            comment5 = Comment(body="Harrison test 5", author_id=self.current_user.id, post_id=post8.id)
            db.session.add(comment1)
            db.session.add(comment2)
            db.session.add(comment3)
            db.session.add(comment4) # Not needed timestamps
            db.session.add(comment5)
            db.session.commit()

            like1 = Like(author_id=self.current_user.id, post_id=post1.id)
            like2 = Like(author_id=self.current_user.id, post_id=post2.id)
            dislike1 = Dislike(author_id=self.current_user.id, post_id=post1.id)
            dislike2 = Dislike(author_id=self.current_user.id, post_id=post2.id)
            db.session.add(like1)
            db.session.add(dislike1)
            db.session.add(like2)
            db.session.add(dislike2)
            db.session.commit()
            
        # FOR ALL CHECKS I ONLY NEED TO CHECK ONE CATEGORY
        # THIS IS BECAUSE EVERYTHING REFERENCES THE CONFIGURATION FILE WITH CATEGORIES

        # Get every post (also newest check)
        result = Post.get_posts_with_comment_status(1, "null", None)
        self.assertEqual(result, [-9, 8, 7, -6, 5, -4, 3, -2, 1])

        # Get every film post (another newest check)
        result = Post.get_posts_with_comment_status(1, "null", 'film')
        self.assertEqual(result, [-9, 7, -6, -4, 3, 1])

        # Check latest
        result = Post.get_posts_with_comment_status(1, "ldst", 'film')
        self.assertEqual(result, [3, -4, -6, 7, -9])

        # Check likes
        result = Post.get_posts_with_comment_status(1, "mslk", None)
        self.assertEqual(result, [1, -2])

        # Check dislikes
        result = Post.get_posts_with_comment_status(1, "msdk", None)
        self.assertEqual(result, [1, -2])

    def test_likes(self):
        with self.app_context:
            post = Post(body="What's a good movie with Harrison Ford?", category='film', user_id=self.current_user.id)
            post1 = Post(body="What's a good movie with Harrison Ford?", category='film', user_id=self.current_user.id)
            comment = Comment(body="Harrison test 1", author_id=self.current_user.id, post_id=post.id)
            comment1 = Comment(body="Harrison test 1", author_id=self.current_user.id, post_id=post.id)
            db.session.add(post)
            db.session.add(comment)
            db.session.add(post1)
            db.session.add(comment1)
            db.session.commit()

        result = self.client.post(f'/like/2/like/post')
        self.assertEqual(result.status_code, 200)

        result = self.client.post(f'/like/2/like/comment')
        self.assertEqual(result.status_code, 200)

        like = Like.query.filter_by(author_id = self.current_user.id, post_id = post1.id).first()
        self.assertEqual(like.author_id, self.current_user.id)

        result = self.client.post(f'/like/2/dislike/post')
        self.assertEqual(result.status_code, 200)

        result = self.client.post(f'/like/2/dislike/comment')
        self.assertEqual(result.status_code, 200)

        like = Dislike.query.filter_by(author_id = self.current_user.id, post_id = post1.id).first()
        self.assertEqual(like.author_id, self.current_user.id)
        post_u = User(id = 24)
        comment_u = User(id = 38)
        post_id = 4
        post_body = "I love Harrison Ford, what's a good movie with him in it?"
        comment_body = "OMG, you HAVE to watch Blade Runner!"
        self.app.post('/newpost', body = post_body, user_id = post_u.id, id = post_id)
        self.app.post('/submit_comment', body = comment_body, author_id = comment_u.id, post_id = post_id)
        comment = db.select(Post).join(Comment).group_by(Post.id).filter_by(author_id=comment_u.id)
        self.assertTrue(comment is not None)

    def test_categories(self):
        post_u = User(id = 24)
        self.app.post('/newpost', body = "any movies with Harrison Ford?", user_id = post_u.id, category = "film")
        self.app.post('/newpost', body = "any video games with Harrison Ford?", user_id = post_u.id, category = "vdga")
        self.app.post('/newpost', body = "any books with Harrison Ford?", user_id = post_u.id, category = "book")
        self.app.post('/newpost', body = "any music with Harrison Ford?", user_id = post_u.id, category = "musc")
        self.app.post('/newpost', body = "any tv shows with Harrison Ford?", user_id = post_u.id, category = "tvsh")

localHost = "http://localhost:5000"

class SeleniumTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(localHost)  

    def test_login_link(self):
        login_link = self.driver.find_element(By.XPATH, "//a[@href='/login']")
        login_link.click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/login"))
        self.assertIn("/login", self.driver.current_url)

    def test_search(self):
        search_input = self.driver.find_element(By.NAME, "searched")
        search_query = "NO POST DATA"
        search_input.send_keys(search_query)
        search_button = self.driver.find_element(By.CLASS_NAME, "search_button")
        search_button.click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/?search_term=NO%20POST%20DATA"))
        expected_url = "/?search_term=NO%20POST%20DATA"
        self.assertIn(expected_url, self.driver.current_url)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)