from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
import time
from db.schemas import *
from db.models import *
from typing import List
from db.sessions import get_db
from celery_tasks.tasks import create_transaction_task
from celery.result import AsyncResult
from celery import current_app

router = APIRouter()


# This is normal function
@router.post("/transactions/", response_model=List[ShowTransaction])
def create_transactions(transactions: List[TransactionCreate], db: Session = Depends(get_db)):
    new_transactions = []
    for transaction in transactions:
        new_transaction = Transaction(company_id=transaction.company_id, product_name=transaction.product_name,
                                      amount=transaction.amount, type=transaction.type)
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        new_transactions.append(new_transaction)
    return new_transactions




# This is async function
@router.post("/async/transactions/", response_model=List[ShowTransaction])
async def create_transactions(transactions: List[TransactionCreate], db: Session = Depends(get_db)):
    new_transactions = []
    for transaction in transactions:
        new_transaction = Transaction(company_id=transaction.company_id, product_name=transaction.product_name,
                                      amount=transaction.amount, type=transaction.type)
        time.sleep(50)
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        new_transactions.append(new_transaction)
    return new_transactions



# need to use celery because the async API is also taking a lot of time. Therefore we will define the API using async function and will return task id as soon as the task is added to the celery queue
@router.post("/celery/async/transactions/", response_model=dict)
async def create_transactions_async(transactions: List[TransactionCreate]):
    transaction_data_list = [transaction.dict() for transaction in transactions]
    task = create_transaction_task.apply_async(args=[transaction_data_list])
    return {"task_id": task.id}



# API to get the result of the task
@router.get("/celery/async/transactions/result/")
async def get_task_result(task_id: str):
    task_result = AsyncResult(task_id, app=current_app)
    if task_result.ready():
        result_value = task_result.result
        return {"status": "completed", "result": result_value}
    else:
        return {"status": "pending"}
    
    
    
@router.get("/list_all_transactions")
def list_all(db: Session  =Depends(get_db)):
    transactions = db.query(Transaction).all()
    
    return transactions







    