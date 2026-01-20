from sqlalchemy import Column, Integer, String
from database import Base

# This represents a TABLE in PostgreSQL
class Item(Base):
    __tablename__ = "items"

    # Column definitions
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
