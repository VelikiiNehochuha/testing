from enum import Enum
from datetime import date

from pydantic import BaseModel


class TransactionType(Enum):
    remove='remove'
    add='add'

class Transaction(BaseModel):
    date: date
    type: TransactionType
    amount_cents: int
    from_id: str
    to_id: str