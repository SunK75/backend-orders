from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.order import Order
from app.schemas.order import OrderCreate



def get_latest_order_id(db: Session):
    latest = db.query(Order).order_by(desc(Order.id)).first()
    return latest.id if latest else 100

def is_order_number_taken(db: Session, order_number: str):
    return db.query(Order).filter(Order.order_number == order_number).first() is not None

def create_order(db: Session, order_data: OrderCreate):
    db_order = Order(**order_data.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_all_orders(db: Session):
    #return db.query(models.Order).order_by(models.Order.id.desc()).all()
    return db.query(Order).order_by(Order.id.desc()).all()

