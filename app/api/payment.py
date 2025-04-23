from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.schemas.payment import (
    PaymentReceivedCreate, PaymentReceivedResponse,
    PaymentMadeCreate, PaymentMadeResponse,
    PaymentResponse, PaymentCreate
)
from app.models.payment import Payment
from app.crud import payment as payment_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Received ---
@router.post("/received", response_model=PaymentReceivedResponse)
def create_payment_received(payment: PaymentReceivedCreate, db: Session = Depends(get_db)):
    return payment_crud.create_payment_received(db, payment)

@router.get("/received", response_model=list[PaymentReceivedResponse])
def list_payments_received(db: Session = Depends(get_db)):
    return payment_crud.get_payments_received(db)

# --- Made ---
@router.post("/made", response_model=PaymentMadeResponse)
def create_payment_made(payment: PaymentMadeCreate, db: Session = Depends(get_db)):
    return payment_crud.create_payment_made(db, payment)

@router.get("/made", response_model=list[PaymentMadeResponse])
def list_payments_made(db: Session = Depends(get_db)):
    return payment_crud.get_payments_made(db)

# --- Generic Payments for Orders ---
@router.get("/by-order/{order_id}", response_model=list[PaymentResponse])
def get_payments_by_order(order_id: int, db: Session = Depends(get_db)):
    #payments = db.query(Payment).filter(Payment.order_id == order_id).all()
    payments = payment_crud.get_payments_by_order(db, order_id)

    if not payments:
        raise HTTPException(status_code=404, detail="No payments found for this order")
    return payments

@router.post("/", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    new_payment = Payment(**payment.dict())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment
