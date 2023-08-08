from .sqlalchemy import Base
from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, DateTime


class Post(Base):
    __tablename__ = "post_req3"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(500), nullable=False)
    published = Column(Boolean, server_default="1", nullable=False, default=True)
    # created_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
