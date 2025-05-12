from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

db = SQLAlchemy()

class Post (db.Model):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column (unique =True, nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            # do not serialize the password, its a security breach
        }

class Users (db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    firtsname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    post: Mapped[List["Posts"]] = relationship(back_populates="users_post")

    author_id: Mapped[List["Comments"]] = relationship(back_populates="author_id")

    followers: Mapped[List["Followers"]] = relationship(back_populates="user_to", foreign_keys="[Followers.user_to_id]")
    following: Mapped[List["Followers"]] = relationship(back_populates="user_from", foreign_keys="[Followers.user_from_id]")
    

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "post": [post.serialize() for post in self.post],
            "author_id": [comment.serialize() for comment in self.author_id],
            "followers": [follower.serialize() for follower in self.followers],
            "following": [followed.serialize() for followed in self.following],
        }

class Comments(db.Model):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(String(200), nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Posts"] = relationship(back_populates="comment_post")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author_id: Mapped["Users"] = relationship(back_populates="comment_user")


    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "post": self.post.title,
            "author_id": self.author_id.username
        }
    
    
class Media(db.Model):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    types: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(80), nullable=False)
    
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post_media: Mapped["Posts"] = relationship(back_populates="media_post")

    def serialize(self):
        return {
            "id": self.id,
            "types": self.types,
            "url": self.url,
            "post_media": self.post_media.serialize()
        }
    
class Followers(db.Model):
    __tablename__ = 'followers'
    user_to_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    date: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)

    user_to: Mapped["Users"] = relationship(back_populates="followers", foreign_keys=[user_to_id])
    user_from: Mapped["Users"] = relationship(back_populates="following", foreign_keys=[user_from_id])

    def serialize(self):
        return {
            "user_to_id": self.user_to_id,
            "user_from_id": self.user_from_id,
            "date": self.date.isoformat()
        }