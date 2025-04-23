from sqlalchemy.orm import Session
from app.models.invoice import SaleInvoice, ExpenseInvoice
from app.schemas.invoice import SaleInvoiceCreate, ExpenseInvoiceCreate

def create_sale_invoice(db: Session, invoice: SaleInvoiceCreate):
    db_invoice = SaleInvoice(**invoice.dict())
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_sale_invoices(db: Session):
    return db.query(SaleInvoice).all()

def create_expense_invoice(db: Session, invoice: ExpenseInvoiceCreate):
    db_invoice = ExpenseInvoice(**invoice.dict())
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_expense_invoices(db: Session):
    return db.query(ExpenseInvoice).all()
