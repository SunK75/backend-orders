import os
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.document import Document

UPLOAD_DIR = "uploaded_docs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
'''
def save_document(db: Session, order_id: int, file: UploadFile):
    ext = file.filename.split(".")[-1]
    unique_filename = f"{uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, unique_filename)

    with open(filepath, "wb") as f:
        content = file.file.read()
        f.write(content)
    
    # ✅ Log file save confirmation
    print(f"✅ File saved to: {filepath}")

    db_doc = Document(order_id=order_id, filename=file.filename, filepath=filepath)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc
'''
def save_document(db: Session, order_id: int, file: UploadFile):
    ext = file.filename.split(".")[-1]
    unique_filename = f"{uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, unique_filename)

    content = file.file.read()
    print("📦 Received file:", file.filename)
    print("✅ Saving to:", filepath)
    print("📏 Size:", len(content), "bytes")

    with open(filepath, "wb") as f:
        f.write(content)

    db_doc = Document(order_id=order_id, filename=file.filename, filepath=filepath)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def get_documents_by_order(db: Session, order_id: int):
    return db.query(Document).filter(Document.order_id == order_id).all()

