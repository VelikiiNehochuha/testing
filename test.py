import unittest
from unittest.mock import patch
from datetime import date
from main import Ctrl
from readers.auto_reader import auto_select_adapter
from readers.adapter import Adapter
from readers.bank_one import BankOneAdapter
from readers.csv_reader import CsvReader
from readers.errors import NoValidAdapter
from transaction import Transaction, TransactionType


def only_one_adapter(path: str) -> Adapter:
    row = next(CsvReader().read(path))
    adapter = BankOneAdapter()
    if adapter.is_valid(row):
        return adapter
    raise NoValidAdapter()


class ConsoleWriter:
    def write(self, transactions: list[Transaction]) -> None:
        print(transactions)


class TestCtrl(unittest.TestCase):

    @patch('builtins.print')
    def test_read_write(self, mock_print):
        ctrl = Ctrl(get_adapter=auto_select_adapter, writer=ConsoleWriter())
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
        ctrl = Ctrl(get_adapter=only_one_adapter, writer=ConsoleWriter())
        self.assertRaises(NoValidAdapter, ctrl.read, 'data/bank2.csv')



unittest.main()