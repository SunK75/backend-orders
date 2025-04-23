from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import invoice, payment, customer, vendor
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/customer/{customer_id}")
def customer_ledger(customer_id: int, db: Session = Depends(get_db)):
    cust = db.query(customer.Customer).filter(customer.Customer.id == customer_id).first()
    if not cust:
        raise HTTPException(status_code=404, detail="Customer not found")

    invoices = db.query(invoice.SaleInvoice).filter(invoice.SaleInvoice.customer_id == customer_id).all()
    payments = db.query(payment.PaymentReceived).filter(payment.PaymentReceived.customer_id == customer_id).all()

    ledger_entries = []

    for inv in invoices:
        ledger_entries.append({
            "date": inv.invoice_date,
            "type": "Invoice",
            "description": inv.description or f"Invoice #{inv.invoice_number}",
            "debit": inv.amount,
            "credit": 0,
        })

    for pay in payments:
        ledger_entries.append({
            "date": pay.received_date,
            "type": "Payment",
            "description": pay.method or "Payment received",
            "debit": 0,
            "credit": pay.amount,
        })

    # Sort by date
    ledger_entries.sort(key=lambda x: x["date"])

    # Add running balance
    balance = 0
    for entry in ledger_entries:
        balance += entry["debit"] - entry["credit"]
        entry["balance"] = balance

    return {
        "customer": cust.name,
        "opening_balance": 0,  # Optional, static for now
        "ledger": ledger_entries,
        "closing_balance": balance
    }

@router.get("/vendor/{vendor_id}")
def vendor_ledger(vendor_id: int, db: Session = Depends(get_db)):
    vend = db.query(vendor.Vendor).filter(vendor.Vendor.id == vendor_id).first()
    if not vend:
        raise HTTPException(status_code=404, detail="Vendor not found")

    invoices = db.query(invoice.ExpenseInvoice).filter(invoice.ExpenseInvoice.vendor_id == vendor_id).all()
    payments = db.query(payment.PaymentMade).filter(payment.PaymentMade.vendor_id == vendor_id).all()

    ledger_entries = []

    for inv in invoices:
        ledger_entries.append({
            "date": inv.invoice_date,
            "type": "Invoice",
            "description": inv.description or f"Invoice #{inv.invoice_number}",
            "debit": inv.amount,
            "credit": 0,
        })

    for pay in payments:
        ledger_entries.append({
            "date": pay.payment_date,
            "type": "Payment",
            "description": pay.method or "Payment made",
            "debit": 0,
            "credit": pay.amount,
        })

    ledger_entries.sort(key=lambda x: x["date"])

    balance = 0
    for entry in ledger_entries:
        balance += entry["debit"] - entry["credit"]
        entry["balance"] = balance

    return {
        "vendor": vend.name,
        "opening_balance": 0,
        "ledger": ledger_entries,
        "closing_balance": balance
    }
