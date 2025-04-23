from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VendorBase(BaseModel):
    name: str
    contact: Optional[str] = None
    gst_number: Optional[str] = None
    address: Optional[str] = None

class VendorCreate(VendorBase):
    pass

class VendorResponse(VendorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
