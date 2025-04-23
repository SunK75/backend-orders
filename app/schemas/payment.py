from pydantic import BaseModel
from typing import Optional
from datetime import date

# --- Payment Received ---
class PaymentReceivedBase(BaseModel):
    customer_id: int
    amount: float
    received_date: Optional[date] = None
    method: Optional[str] = None
    invoice_id: Optional[int] = None

class PaymentReceivedCreate(PaymentReceivedBase):
    pass

class PaymentReceivedResponse(PaymentReceivedBase):
    id: int

    class Config:
        from_attributes = True


# --- Payment Made ---
class PaymentMadeBase(BaseModel):
    vendor_id: int
    amount: float
    payment_date: Optional[date] = None
    method: Optional[str] = None
    invoice_id: Optional[int] = None

class PaymentMadeCreate(PaymentMadeBase):
    pass

class PaymentMadeResponse(PaymentMadeBase):
    id: int

    class Config:
        from_attributes = True


# --- Generic Order Payments ---
class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    date: date
    type: str  # "customer" or "vendor"

class PaymentResponse(BaseModel):  # ✅ Clean, unified response schema
    id: int
    order_id: int
    amount: float
    date: date
    type: str

    class Config:
        from_attributes = True
