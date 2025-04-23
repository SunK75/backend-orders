from sqlalchemy.orm import Session
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate

def create_vendor(db: Session, vendor: VendorCreate):
    db_vendor = Vendor(**vendor.dict())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

def get_vendors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Vendor).offset(skip).limit(limit).all()

def get_vendor(db: Session, vendor_id: int):
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()

def update_vendor(db: Session, vendor_id: int, vendor: VendorCreate):
    db_vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if db_vendor is None:
        return None
    for key, value in vendor.dict().items():
        setattr(db_vendor, key, value)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

def delete_vendor(db: Session, vendor_id: int):
    db_vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if db_vendor is None:
        return False
    db.delete(db_vendor)
    db.commit()
    return True



'''
from sqlalchemy.orm import Session
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate

def create_vendor(db: Session, vendor: VendorCreate):
    db_vendor = Vendor(**vendor.dict())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

def get_vendors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Vendor).offset(skip).limit(limit).all()

def get_vendor(db: Session, vendor_id: int):
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()
'''