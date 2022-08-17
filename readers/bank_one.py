import csv
from logging import getLogger
from enum import Enum
from datetime import datetime
from decimal import Decimal
from typing import Dict, Any

from pydantic import BaseModel, validator
from pydantic.fields import Field

from transaction import Transaction
from pydantic import ValidationError


logger = getLogger(__name__)


class TransactionType(Enum):
    remove='remove'
    add='add'

class BankOneRow(BaseModel):
    datestr: str = Field(alias='timestamp')
    type: TransactionType
    amount: Decimal
    to_id: str = Field(alias='to')
    from_id: str = Field(alias='from')

    @classmethod
    @validator('datestr')
    def datestr_valid(cls, value):
        try:
            datetime.strptime(value, '%b %d %Y')
        except ValueError:
            raise ValidationError(f'not valid field: timestamp value: {value}')

    def to_transaction(self) -> Transaction:
        return Transaction(
            date=datetime.strptime(self.datestr, '%b %d %Y'),
            type=self.type.name,
            amount_cents=int(self.amount * 100),
            to_id=self.to_id,
            from_id=self.from_id,
        )

class BankOneAdapter:
    def is_valid(self, row: Dict[str, Any]) -> bool:
        try:
            BankOneRow(**row).to_transaction()
            return True
        except ValidationError as err:
            logger.debug(err)
        return False

    def transform(self, row: Dict[str, Any]) -> Transaction:
        return BankOneRow(**row).to_transaction()
