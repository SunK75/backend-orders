from datetime import date as dt_date
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class InvoiceStatus(str, Enum):
    unpaid = "unpaid"
    paid = "paid"
    partial = "partial"


class SaleInvoiceBase(BaseModel):
    customer_id: int
    invoice_number: Optional[str] = None
    invoice_date: Optional[dt_date] = Field(default_factory=dt_date.today)  # ✅ renamed
    amount: float
    description: Optional[str] = None
    due_date: Optional[dt_date] = None
    status: InvoiceStatus = InvoiceStatus.unpaid


class SaleInvoiceCreate(SaleInvoiceBase):
    pass

class SaleInvoiceResponse(SaleInvoiceBase):
    id: int
    model_config = {
        "from_attributes": True
    }


class ExpenseInvoiceBase(BaseModel):
    vendor_id: int
    invoice_number: Optional[str] = None
    invoice_date: Optional[dt_date] = Field(default_factory=dt_date.today)  # ✅ renamed
    amount: float
    description: Optional[str] = None
    due_date: Optional[dt_date] = None
    status: InvoiceStatus = InvoiceStatus.unpaid

class ExpenseInvoiceCreate(ExpenseInvoiceBase):
    pass

class ExpenseInvoiceResponse(ExpenseInvoiceBase):
    id: int
    model_config = {
        "from_attributes": True
    }
