# api/invoice.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.schemas.invoice import (
    SaleInvoiceCreate, SaleInvoiceResponse,
    ExpenseInvoiceCreate, ExpenseInvoiceResponse
)
from app.crud import invoice as invoice_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Sale Invoices
@router.post("/sales", response_model=SaleInvoiceResponse)
def create_sale_invoice(payload: SaleInvoiceCreate, db: Session = Depends(get_db)):
    return invoice_crud.create_sale_invoice(db=db, invoice=payload)

@router.get("/sales", response_model=list[SaleInvoiceResponse])
def read_sale_invoices(db: Session = Depends(get_db)):
    return invoice_crud.get_sale_invoices(db)

# ✅ Expense Invoices
@router.post("/expenses", response_model=ExpenseInvoiceResponse)
def create_expense_invoice(payload: ExpenseInvoiceCreate, db: Session = Depends(get_db)):
    return invoice_crud.create_expense_invoice(db=db, invoice=payload)

@router.get("/expenses", response_model=list[ExpenseInvoiceResponse])
def read_expense_invoices(db: Session = Depends(get_db)):
    return invoice_crud.get_expense_invoices(db)
