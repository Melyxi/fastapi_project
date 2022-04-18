from typing import List

from fastapi import APIRouter, Depends

from endpoints.depends import get_transaction_repository
from models.transaction import TransactionIn, Transaction, TransactionUpdate
from repositories.transaction import TransactionRepository

router = APIRouter()


@router.post("/", response_model=Transaction)
async def post_transaction(
        transaction: TransactionIn,
        transactions: TransactionRepository = Depends(get_transaction_repository)):
    return await transactions.create_transaction(t=transaction)


@router.get("/", response_model=List[Transaction])
async def get_transaction(
        transactions: TransactionRepository = Depends(get_transaction_repository), ):
    return await transactions.get_transaction_waiting()


@router.put("/{id}/", response_model=Transaction)
async def update_transaction(id: int,
                             transaction: TransactionUpdate,
                             transactions: TransactionRepository = Depends(get_transaction_repository), ):
    return await transactions.update_transaction(id=id, t=transaction)
