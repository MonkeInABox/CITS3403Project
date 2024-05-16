from datetime import datetime, timezone
from flask import current_app, request
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from app import db
from itsdangerous import URLSafeTimedSerializer

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.Mapped[list['Post']] = so.relationship('Post', back_populates='author', lazy="dynamic", cascade="all, delete-orphan")
    
    user_comments: so.Mapped['Comment'] = so.relationship(back_populates="commenter", cascade="all, delete-orphan")

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
    
    def generate_password_reset_token(email):
        # Generate a token that expires in 1 hour (3600 seconds)
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(email, salt='password-reset-salt')

    def confirm_password_reset_token(token, max_age=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            # Load and validate the token
            email = serializer.loads(token, salt='password-reset-salt', max_age=max_age)
            return email
        except Exception:
            return None
        
    

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    body: so.Mapped[str] = so.mapped_column(sa.String(200))

    category: so.Mapped[str] = so.mapped_column(sa.String(4), index=True)

    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    comments: so.Mapped[list['Comment']] = so.relationship('Comment', back_populates='original_post', cascade="all, delete-orphan")

    likes: so.Mapped[list['Like']] = so.relationship('Like', back_populates='original_post', cascade="all, delete-orphan")

    dislikes: so.Mapped[list['Dislike']] = so.relationship('Dislike', back_populates='original_post', cascade="all, delete-orphan")

    def __init__(self, body: str, user_id: int, category: str):
        self.body = body
        self.user_id = user_id
        self.category = category

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    
    def get_posts_by_cat(category):
        page = request.args.get('page', 1, type=int)
        query = sa.select(Post).filter_by(category=category).order_by(Post.timestamp.desc())
        posts = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
        return posts
    
    def get_posts_by_cat_filter(category, filter):
        page = request.args.get('page', 1, type=int)
        if filter == "nwst":
            query = sa.select(Post).filter_by(category=category).order_by(Post.timestamp.desc())
        elif filter == "ldst":
            query = sa.select(Post).filter_by(category=category).order_by(Post.timestamp.asc())
        elif filter == "mslk":
            query = sa.select(Post).filter_by(category=category).join(Post.likes).group_by(Post.id).order_by(db.func.count(Post.likes).desc())
        elif filter == "msdk":
            query = sa.select(Post).filter_by(category=category).join(Post.dislikes).group_by(Post.id).order_by(db.func.count(Post.dislikes).desc())
        elif filter == "mscm":
            query = sa.select(Post).filter_by(category=category).join(Post.comments).group_by(Post.id).order_by(db.func.count(Post.comments).desc())
        posts = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
        return posts
    
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
class Comment(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    body: so.Mapped[str] = so.mapped_column(sa.String(200))

    author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    commenter: so.Mapped[User] = so.relationship('User', back_populates="user_comments")

    post_id = so.mapped_column(sa.ForeignKey('post.id'), index=True)
    
    original_post = db.relationship('Post', back_populates='comments')

    likes: so.Mapped[list['Like']] = so.relationship('Like', back_populates='original_comment', cascade="all, delete-orphan")

    dislikes: so.Mapped[list['Dislike']] = so.relationship('Dislike', back_populates='original_comment', cascade="all, delete-orphan")

    def __init__(self, body: str, author_id: int, post_id: int):
        self.body = body
        self.author_id = author_id
        self.post_id = post_id

class Like(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    post_id = so.mapped_column(sa.ForeignKey('post.id'), index=True)

    original_post = db.relationship('Post', back_populates='likes')

    comment_id = so.mapped_column(sa.ForeignKey('comment.id'), index=True)

    original_comment = db.relationship('Comment', back_populates='likes')


class Dislike(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    post_id = so.mapped_column(sa.ForeignKey('post.id'), index=True)

    original_post = db.relationship('Post', back_populates='dislikes')

    comment_id = so.mapped_column(sa.ForeignKey('comment.id'), index=True)

    original_comment = db.relationship('Comment', back_populates='dislikes')


    


    