from sqlalchemy.orm import Session
from app.models.payment import PaymentReceived, PaymentMade, Payment
from app.schemas.payment import PaymentReceivedCreate, PaymentMadeCreate, PaymentCreate

# --- Received ---
def create_payment_received(db: Session, payment: PaymentReceivedCreate):
    db_payment = PaymentReceived(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payments_received(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PaymentReceived).offset(skip).limit(limit).all()

# --- Made ---
def create_payment_made(db: Session, payment: PaymentMadeCreate):
    db_payment = PaymentMade(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payments_made(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PaymentMade).offset(skip).limit(limit).all()

def create_order_payment(db: Session, payment: PaymentCreate):
    db_payment = Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payments_by_order(db: Session, order_id: int):
    return db.query(Payment).filter(Payment.order_id == order_id).all()

def upsert_order_payment(db: Session, payment: PaymentCreate):
    from app.models.payment import Payment

    if hasattr(payment, "id") and payment.id:
        db_payment = db.query(Payment).filter(Payment.id == payment.id).first()
        if db_payment:
            db_payment.amount = payment.amount
            db_payment.date = payment.date
            db_payment.type = payment.type
            db.commit()
            db.refresh(db_payment)
            return db_payment

    # Else create new payment
    db_payment = Payment(**payment.dict(exclude={"id"}))
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

