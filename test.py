#!/usr/bin/env python
import unittest
import multiprocessing
from app import create_app, db
from app.models import User, Post, Comment
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

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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
        u = User(id = 24)
        post_body = "I love Harrison Ford, what's a good movie with him in it?"
        self.app.post('/newpost', body = post_body, user_id = u.id)
        post = db.select(Post).filter_by(user_id=u.id)
        self.assertTrue(post is not None)
    
    def test_comment(self):
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
        print(self.app.get('categories/film'))

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