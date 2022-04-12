import sqlalchemy
from .base import metadata
import datetime
import enum


class TransactionEnum(str, enum.Enum):
    withdrawal = "withdrawal"
    deposit = "deposit"


class TransactionStatusEnum(enum.Enum):
    waiting = "waiting"
    completed = "completed"
    failed = "failed"

transactions = sqlalchemy.Table(
    "transactions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("id_user", sqlalchemy.Integer),
    sqlalchemy.Column("transfer_amount", sqlalchemy.Integer),
    sqlalchemy.Column("transfer_choice", sqlalchemy.Enum(TransactionEnum)),
    sqlalchemy.Column("transfer_status", sqlalchemy.Enum(TransactionStatusEnum)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow)
)
