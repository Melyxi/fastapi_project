import datetime
from typing import Optional
from pydantic import BaseModel, conint
from db.transaction import TransactionEnum, TransactionStatusEnum


class Transaction(BaseModel):
    id: Optional[str] = None
    id_user: int
    transfer_amount: conint(gt=0)
    transfer_choice: TransactionEnum
    transfer_status: TransactionStatusEnum
    created_at: datetime.datetime
    updated_at: datetime.datetime


class TransactionIn(BaseModel):
    id_user: int
    transfer_amount: conint(gt=0)
    transfer_choice: TransactionEnum

class TransactionUpdate(BaseModel):
    transfer_status: TransactionStatusEnum
