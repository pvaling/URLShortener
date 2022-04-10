from sqlalchemy import Column, Integer, String

from .database import Base


class ShortUrl(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short = Column(String, unique=True, index=True)
    url = Column(String)

    
