from db.base import database
from repositories.transaction import TransactionRepository


def get_transaction_repository() -> TransactionRepository:
    return TransactionRepository(database)