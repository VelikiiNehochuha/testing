import csv
from logging import getLogger
from enum import Enum
from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, validator
from pydantic.fields import Field

from transaction import Transaction
from pydantic import ValidationError


logger = getLogger(__name__)


class TransactionType(Enum):
    remove='remove'
    add='add'

class BankThreeRow(BaseModel):
    date_readable: str = Field(alias='date_readable')
    type: TransactionType
    euro: int
    cents: int
    to_id: str = Field(alias='to')
    from_id: str = Field(alias='from')

    @classmethod
    @validator('datestr')
    def datestr_valid(cls, value):
        try:
            datetime.strptime(value, '%d %b %Y')
        except ValueError:
            raise ValidationError(f'not valid field: timestamp value: {value}')

    def to_transaction(self) -> Transaction:
        return Transaction(
            date=datetime.strptime(self.date_readable, '%d %b %Y'),
            type=self.type.name,
            amount_cents=int(self.euro * 100 + self.cents),
            to_id=self.to_id,
            from_id=self.from_id,
        )


class BankThreeAdapter:
    def is_valid(self, row: Dict[str, Any]) -> bool:
        try:
            BankThreeRow(**row).to_transaction()
            return True
        except ValidationError as err:
            logger.debug(err)
        return False

    def transform(self, row: Dict[str, Any]) -> Transaction:
        return BankThreeRow(**row).to_transaction()