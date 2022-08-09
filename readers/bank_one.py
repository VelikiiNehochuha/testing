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


class BankOneReader:
    def is_valid(self, path: str) -> bool:
        with open(path) as csv_file:
            reader = csv.DictReader(csv_file)
            try:
                BankOneRow(**next(reader)).to_transaction()
            except ValidationError as err:
                logger.warning('Not valid reader for the file, try another one %s', err)
                return False
        return True

    def read(self, path: str) -> list[Transaction]:
        with open(path) as csv_file:
            reader = csv.DictReader(csv_file)
            return [BankOneRow(**row).to_transaction() for row in reader]