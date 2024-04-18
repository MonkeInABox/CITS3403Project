from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from app import db

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.Mapped['Post'] = so.relationship(back_populates='author')
    
    user_comments: so.Mapped['Comment'] = so.relationship(back_populates="commenter")

    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    body: so.Mapped[str] = so.mapped_column(sa.String(200))

    category: so.Mapped[str] = so.mapped_column(sa.String(40), index=True)

    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    comments = db.relationship('Comment', back_populates='original_post')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    
    
    
class Comment(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    body: so.Mapped[str] = so.mapped_column(sa.String(200))

    author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    commenter: so.Mapped[User] = so.relationship(back_populates="user_comments")

    post_id = so.mapped_column(sa.ForeignKey('post.id'), index=True)

    original_post = db.relationship('Post', back_populates='comments')
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))