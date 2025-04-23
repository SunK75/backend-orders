from pydantic import BaseModel
from datetime import date
from typing import Optional

class OrderBase(BaseModel):
    order_number: str
    date: date
    status: Optional[str] = "Open"
    payment_status: Optional[str] = "Unpaid"

    customer_name: str
    customer_contact: str
    customer_rate: int
    customer_expenses: Optional[str]

    transporter_name: str
    transporter_contact: str
    transporter_rate: int
    transporter_expenses: Optional[str]

    from_location: str
    to_location: str

    vehicle_number: Optional[str]
    driver_name: Optional[str]
    driver_contact: Optional[str]

class OrderCreate(OrderBase):
    pass

class OrderOut(OrderBase):
    id: int

class OrderUpdate(BaseModel):
    vehicle_number: Optional[str]
    driver_name: Optional[str]
    driver_contact: Optional[str]
    from_location: Optional[str]
    to_location: Optional[str]

    class Config:
        from_attributes = True  # for Pydantic v2+
