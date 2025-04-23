from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from datetime import date
from app.db import Base

class PaymentReceived(Base):
    __tablename__ = "payments_received"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    amount = Column(Float, nullable=False)
    received_date = Column(Date, default=date.today)
    method = Column(String)
    invoice_id = Column(Integer, ForeignKey("sale_invoices.id"), nullable=True)

class PaymentMade(Base):
    __tablename__ = "payments_made"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    amount = Column(Float, nullable=False)
    payment_date = Column(Date, default=date.today)
    method = Column(String)
    invoice_id = Column(Integer, ForeignKey("expense_invoices.id"), nullable=True)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    type = Column(String, nullable=False)  # "customer" or "vendor"
