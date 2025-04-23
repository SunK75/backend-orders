from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Enum
from datetime import date
from app.db import Base
import enum

class InvoiceStatus(enum.Enum):
    unpaid = "unpaid"
    paid = "paid"
    partial = "partial"

class SaleInvoice(Base):
    __tablename__ = "sale_invoices"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    invoice_number = Column(String)
    invoice_date = Column(Date, default=date.today)
    amount = Column(Float)
    description = Column(String)
    due_date = Column(Date)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.unpaid)

class ExpenseInvoice(Base):
    __tablename__ = "expense_invoices"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    invoice_number = Column(String)
    invoice_date = Column(Date, default=date.today)
    amount = Column(Float)
    description = Column(String)
    due_date = Column(Date)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.unpaid)
