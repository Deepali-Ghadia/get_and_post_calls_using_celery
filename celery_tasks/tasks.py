from typing import List, Optional
from fastapi import Depends
from time import sleep
from celery import shared_task
from celery.result import AsyncResult
from celery import current_app
from sqlalchemy.orm import Session
from db.models import *
from db.schemas import *
from db.sessions import get_db
import time

@shared_task
def create_transaction_task(transactions: List[dict]):  # Change the argument type to List[dict]
    with Session() as db:
        new_transactions = []
        for transaction_data in transactions:
            transaction = TransactionCreate(**transaction_data)  # Convert the dictionary back to TransactionCreate object
            new_transaction = Transaction(
                company_id=transaction.company_id,
                product_name=transaction.product_name,
                amount=transaction.amount,
                type=transaction.type
            )
            # time.sleep(50)  # Simulate some time-consuming task
            db.add(new_transaction)
            db.commit()
            db.refresh(new_transaction)
            new_transactions.append(new_transaction)
        return new_transactions
# def create_transaction_task(transactions: List[dict]):
#     with Session() as db:
#         new_transactions = []
#         for transaction_data in transactions:
#             transaction = TransactionCreate(**transaction_data)
#             new_transaction = Transaction(
#                 company_id=transaction.company_id,
#                 product_name=transaction.product_name,
#                 amount=transaction.amount,
#                 type=transaction.type
#             )
#             new_transactions.append(new_transaction)

#         db.add_all(new_transactions)  # Batch insert all transactions
#         db.commit()  # Commit the batch insert
#         db.refresh_all(new_transactions)  # Refresh all newly added transactions

#     return new_transactions