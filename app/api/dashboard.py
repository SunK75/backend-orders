from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.invoice import SaleInvoice, ExpenseInvoice
from app.models.payment import PaymentReceived, PaymentMade
from sqlalchemy import func
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    # Totals
    total_sales = db.query(func.coalesce(func.sum(SaleInvoice.amount), 0)).scalar()
    total_expenses = db.query(func.coalesce(func.sum(ExpenseInvoice.amount), 0)).scalar()
    total_received = db.query(func.coalesce(func.sum(PaymentReceived.amount), 0)).scalar()
    total_paid = db.query(func.coalesce(func.sum(PaymentMade.amount), 0)).scalar()

    # Outstanding
    receivables = total_sales - total_received
    payables = total_expenses - total_paid

    return {
        "total_sales": total_sales,
        "total_expenses": total_expenses,
        "payments_received": total_received,
        "payments_made": total_paid,
        "cash_flow": total_received - total_paid,
        "receivables": receivables,
        "payables": payables
    }
