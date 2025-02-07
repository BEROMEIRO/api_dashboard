from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)  
    category = Column(String)
    created_at = Column(DateTime, server_default=func.now())  
