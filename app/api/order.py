from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate
from app.schemas.payment import PaymentCreate
from app.crud.payment import upsert_order_payment
from app.crud import order as crud_order
from app.crud import payment as crud_payment
from app.db import get_db
from app.models.order import Order
from app.crud.document import get_documents_by_order
from app.schemas.document import DocumentResponse

router = APIRouter()

@router.get("/latest-id")
def get_latest_order_id(db: Session = Depends(get_db)):
    latest_id = crud_order.get_latest_order_id(db)
    return {"latest_id": latest_id}


@router.get("/", response_model=List[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return crud_order.get_all_orders(db)


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        if crud_order.is_order_number_taken(db, order.order_number):
            raise HTTPException(status_code=400, detail="Order number already exists")
        return crud_order.create_order(db, order)
    except Exception as e:
        print("Create Order Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.patch("/{order_id}", response_model=OrderOut)
def update_order(
    order_id: int,
    update_data: OrderUpdate,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order


@router.post("/{order_id}/payments")
def save_order_payments(order_id: int, payments: List[PaymentCreate], db: Session = Depends(get_db)):
    for p in payments:
        crud_payment.create_order_payment(db, PaymentCreate(**p.dict(), order_id=order_id))
    return {"status": "success"}


@router.post("/{order_id}/documents")
def upload_documents(order_id: int, files: List[UploadFile] = File(...)):
    uploaded = []
    for file in files:
        file_location = f"uploads/{order_id}_{file.filename}"
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        uploaded.append({"name": file.filename, "url": f"/{file_location}"})
    return uploaded

@router.get("/{order_id}/documents", response_model=List[DocumentResponse])
def get_order_documents(order_id: int, db: Session = Depends(get_db)):
    return get_documents_by_order(db, order_id)



'''
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate  # ✅ Include OrderUpdate
from app.crud import order as crud_order
from app.db import get_db
from app.models.order import Order  # ✅ Needed for patch operation

router = APIRouter()

@router.get("/latest-id")
def get_latest_order_id(db: Session = Depends(get_db)):
    latest_id = crud_order.get_latest_order_id(db)
    return {"latest_id": latest_id}


@router.get("/", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return crud_order.get_all_orders(db)


@router.post("/", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        if crud_order.is_order_number_taken(db, order.order_number):
            raise HTTPException(status_code=400, detail="Order number already exists")
        return crud_order.create_order(db, order)
    except Exception as e:
        print("Create Order Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


# ✅ NEW: PATCH endpoint to update selected fields of an order
@router.patch("/{order_id}", response_model=OrderOut)
def update_order(order_id: int, update_data: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order


@router.get("/{order_id}", response_model=OrderOut)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
'''

