from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact = Column(String)
    gst_number = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
