from sqlalchemy import Column, Integer, String, Date
from app.db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True)
    date = Column(Date)
    status = Column(String, default="Open")
    payment_status = Column(String, default="Unpaid")

    customer_name = Column(String)
    customer_contact = Column(String)
    customer_rate = Column(Integer)
    customer_expenses = Column(String)

    transporter_name = Column(String)
    transporter_contact = Column(String)
    transporter_rate = Column(Integer)
    transporter_expenses = Column(String)

    from_location = Column(String)
    to_location = Column(String)

    vehicle_number = Column(String)
    driver_name = Column(String)
    driver_contact = Column(String)

