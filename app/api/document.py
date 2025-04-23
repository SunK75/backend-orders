from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os, uuid

from app.db import get_db
from app.schemas.document import DocumentResponse
from app.crud.document import save_document

router = APIRouter()
UPLOAD_DIR = "uploaded_docs"

@router.post("/upload", response_model=List[DocumentResponse])
def uploaded_docs(
    order_id: int = Form(...),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):

    print("📥 /upload called")
    print("📌 Received order_id:", order_id)
    print("📁 Files received:", [f.filename for f in files])
    
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    saved_docs = []
    for file in files:
        if not file.filename:
            continue
        doc = save_document(db, order_id, file)
        saved_docs.append(doc)

    return saved_docs

