from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import customer as customer_api
from app.api import vendor as vendor_api
from app.api import dashboard as dashboard_api
from app.db import Base, engine
from app.models import customer as customer_model
from app.models import vendor as vendor_model  # ✅ Add this
from app.api import invoice as invoice_api
from app.models import invoice as invoice_model  # needed for table creation
from app.api import payment as payment_api
from app.models import payment as payment_model
from app.api import ledger as ledger_api
from app.api import order as order_api
from app.models import order as order_model
from app.api import document as document_api



Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(customer_api.router, prefix="/customers", tags=["Customers"])
app.include_router(vendor_api.router, prefix="/vendors", tags=["Vendors"])  # ✅ Add this
app.include_router(invoice_api.router, prefix="/invoices", tags=["Invoices"])
app.include_router(payment_api.router, prefix="/payments", tags=["Payments"])
app.include_router(ledger_api.router, prefix="/ledger", tags=["Ledger"])
app.include_router(dashboard_api.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(order_api.router, prefix="/orders", tags=["Orders"])
app.include_router(document_api.router, prefix="/documents", tags=["Documents"])

# ✅ Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def test_root():
    return {"message": "Hello from backend"}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import customer as customer_api
from app.api import vendor as vendor_api
from app.api import dashboard as dashboard_api
from app.db import Base, engine
from app.models import customer as customer_model
from app.models import vendor as vendor_model
from app.api import invoice as invoice_api
from app.models import invoice as invoice_model
from app.api import payment as payment_api
from app.models import payment as payment_model
from app.api import ledger as ledger_api
from app.api import order as order_api
from app.models import order as order_model
from app.api import document as document_api

# ✅ Migrate tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Routers
app.include_router(customer_api.router, prefix="/customers", tags=["Customers"])
app.include_router(vendor_api.router, prefix="/vendors", tags=["Vendors"])
app.include_router(invoice_api.router, prefix="/invoices", tags=["Invoices"])
app.include_router(payment_api.router, prefix="/payments", tags=["Payments"])
app.include_router(ledger_api.router, prefix="/ledger", tags=["Ledger"])
app.include_router(dashboard_api.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(order_api.router, prefix="/orders", tags=["Orders"])
app.include_router(document_api.router, prefix="/documents", tags=["Documents"])

# ✅ Enable CORS for local + deployed frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "https://frontend-orders.onrender.com"  # <-- replace with actual Render frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def test_root():
    return {"message": "Hello from backend"}
