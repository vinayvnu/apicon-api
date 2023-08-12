from .sqlalchemy import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import DateTime


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(500), nullable=False)
    published = Column(Boolean, server_default="1", nullable=False, default=True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    # below code will create a property for the post, so when we retrieve a post its going to
    # retrieve owner property and its going to figure out the relationship.
    # Users passesd is the class name not the table name.
    owner = relationship("Users")


class Users(Base):
    __tablename__ = "users"
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False, unique=True)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    name = Column(String(255), nullable=False, unique=True)


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
