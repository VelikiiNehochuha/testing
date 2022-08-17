from logging import getLogger
from enum import Enum
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict

from pydantic import BaseModel, validator
from pydantic.fields import Field

from transaction import Transaction
from pydantic import ValidationError


logger = getLogger(__name__)


class TransactionType(Enum):
    remove='remove'
    add='add'

class BankTwoRow(BaseModel):
    date: str = Field(alias='date')
    type: TransactionType = Field(alias='transaction')
    amounts: Decimal
    to_id: str = Field(alias='to')
    from_id: str = Field(alias='from')

    @classmethod
    @validator('date')
    def date_valid(cls, value):
        try:
            datetime.strptime(value, '%d-%m-%Y')
        except ValueError as err:
            logger.warning(err)
            raise ValidationError(f'not valid field: date, value: {value}')

    def to_transaction(self) -> Transaction:
        return Transaction(
            date=datetime.strptime(self.date, '%d-%m-%Y'),
            type=self.type.name,
            amount_cents=int(self.amounts * 100),
            to_id=self.to_id,
            from_id=self.from_id,
        )


class BankTwoAdapter:
    def is_valid(self, row: Dict[str, Any]) -> bool:
        try:
            BankTwoRow(**row).to_transaction()
            return True
        except ValidationError as err:
            logger.debug(err)
        return False

    def transform(self, row: Dict[str, Any]) -> Transaction:
        return BankTwoRow(**row).to_transaction()
