#!/usr/bin/env python
import unittest
from app import create_app, db
from app.models import User, Post, Comment
from config import Config
from app.posts.forms import PostNewPost

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
        self.app.post('/submit_comment', body = post_body, user_id = post_u.id, id = post_id)
        self.app.post('/newcomment', body = comment_body, author_id = comment_u.id, post_id = post_id)
        comment = db.select(Post).join(Comment).group_by(Post.id).filter_by(author_id=comment_u.id)
        self.assertTrue(comment is not None)

        
if __name__ == '__main__':
    unittest.main(verbosity=2)