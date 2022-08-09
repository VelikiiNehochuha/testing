import csv
from logging import getLogger
from enum import Enum
from datetime import datetime
from decimal import Decimal

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


class BankTwoReader:
    def is_valid(self, path: str) -> bool:
        with open(path) as csv_file:
            reader = csv.DictReader(csv_file)
            try:
                BankTwoRow(**next(reader)).to_transaction()
            except ValidationError as err:
                logger.warning('Not valid reader for the file, try another one %s', err)
                return False
        return True

    def read(self, path: str) -> list[Transaction]:
        with open(path) as csv_file:
            reader = csv.DictReader(csv_file)
            return [BankTwoRow(**row).to_transaction() for row in reader]