import datetime
from typing import List, Optional
from sqlalchemy import text

from db.transaction import TransactionStatusEnum, transactions
from models.transaction import TransactionIn, Transaction, TransactionUpdate
from .base import BaseRepository


class TransactionRepository(BaseRepository):
    async def create_transaction(self, t: TransactionIn) -> Transaction:
        transaction = Transaction(
            id=0,
            id_user=t.id_user,
            transfer_amount=t.transfer_amount,
            transfer_choice=t.transfer_choice,
            transfer_status=TransactionStatusEnum.waiting,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        values = {**transaction.dict()}
        values.pop("id", None)
        query = transactions.insert().values(**values)
        transaction.id = await self.database.execute(query)
        return transaction

    async def get_transaction_waiting(self) -> List[Transaction]:
        query = transactions.select().where(transactions.c.transfer_status == TransactionStatusEnum.waiting).order_by(text('id asc'))
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> Optional[Transaction]:
        query = transactions.select().where(transactions.c.id == id)
        transaction = await self.database.fetch_one(query=query)
        if transaction is None:
            return None
        return Transaction.parse_obj(transaction)

    async def update_transaction(self, id: int, t: TransactionUpdate) -> Transaction:
        tr = await self.get_by_id(id)

        transaction = Transaction(
            id=id,
            id_user=tr.id_user,
            transfer_amount=tr.transfer_amount,
            transfer_choice=tr.transfer_choice,
            transfer_status=t.transfer_status,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        values = {**transaction.dict()}

        values.pop("id", None)
        values.pop("id_user", None)
        values.pop("transfer_amount", None)
        values.pop("created_at", None)

        query = transactions.update().where(transactions.c.id == id).values(**values)
        await self.database.execute(query)
        return transaction
