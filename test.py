import unittest
from unittest.mock import patch
from datetime import date
from pydantic import ValidationError
from main import Ctrl
from readers.auto_reader import auto_select_reader
from readers.reader import Reader
from readers.bank_one import BankOneReader
from readers.errors import NoValidReader
from transaction import Transaction, TransactionType


def only_one_reader(path: str) -> Reader:
    reader = BankOneReader()
    if reader.is_valid(path):
        return reader
    raise NoValidReader()


class ConsoleWriter:
    def write(self, transactions: list[Transaction]) -> None:
        print(transactions)


class TestCtrl(unittest.TestCase):

    @patch('builtins.print')
    def test_read_write(self, mock_print):
        ctrl = Ctrl(get_reader=auto_select_reader, writer=ConsoleWriter())
        ctrl.read('data/bank1.csv')
        ctrl.write()
        mock_print.assert_called_with(
            [
                Transaction(
                    date=date(2019, 10, 1),
                    type=TransactionType.remove,
                    amount_cents=9910,
                    from_id='198 ',
                    to_id='182',
                ),
                Transaction(
                    date=date(2019, 10, 2),
                    type=TransactionType.add,
                    amount_cents=200010,
                    from_id='188',
                    to_id='198',
                )
            ]
        )

    def test_read_error_with_one_bank(self):
        ctrl = Ctrl(get_reader=only_one_reader, writer=ConsoleWriter())
        self.assertRaises(NoValidReader, ctrl.read, 'data/bank2.csv')

    def test_validation_error(self):
        reader = BankOneReader()
        self.assertRaises(ValidationError, reader.read, 'data/bank2.csv')


unittest.main()