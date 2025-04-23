from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
