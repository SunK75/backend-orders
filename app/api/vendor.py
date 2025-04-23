from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.schemas.vendor import VendorCreate, VendorResponse
from app.crud import vendor as vendor_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=VendorResponse)
def create_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    return vendor_crud.create_vendor(db, vendor)

@router.get("/", response_model=list[VendorResponse])
def read_vendors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return vendor_crud.get_vendors(db, skip, limit)

@router.get("/{vendor_id}", response_model=VendorResponse)
def read_vendor(vendor_id: int, db: Session = Depends(get_db)):
    db_vendor = vendor_crud.get_vendor(db, vendor_id)
    if not db_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor

@router.put("/{vendor_id}", response_model=VendorResponse)
def update_vendor(vendor_id: int, vendor: VendorCreate, db: Session = Depends(get_db)):
    db_vendor = vendor_crud.update_vendor(db, vendor_id, vendor)
    if not db_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor

@router.delete("/{vendor_id}")
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)):
    success = vendor_crud.delete_vendor(db, vendor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"message": "Vendor deleted successfully"}
