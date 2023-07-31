from pydantic import BaseModel
from datetime import datetime
class TransactionCreate(BaseModel):
    company_id: int
    product_name: str
    amount: int
    type: str
    
    class Config:
        orm_mode = True
        
class ShowTransaction(BaseModel):
    id: int
    company_id: int
    product_name: str
    amount: int
    time: datetime
    type: str
    
    class Config:
        orm_mode = True