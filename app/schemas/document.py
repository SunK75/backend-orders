from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: int
    order_id: int
    filename: str
    filepath: str

    class Config:
        from_attributes = True
