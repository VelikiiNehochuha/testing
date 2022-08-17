from typing import Callable, Iterable

from readers.bank_one import BankOneAdapter
from readers.bank_two import BankTwoAdapter
from readers.bank_three import BankThreeAdapter
from readers.adapter import Adapter
from readers.errors import NoValidAdapter

from readers.csv_reader import CsvReader
from transaction import Transaction

ADAPTERS_CLASSES = (
    BankOneAdapter,
    BankTwoAdapter,
    BankThreeAdapter,
)

AutoReader = Callable[[str], Adapter]

def auto_select_adapter(path: str) -> Adapter:
    row = next(CsvReader().read(path))
    for adapter_class in ADAPTERS_CLASSES:
        adapter = adapter_class()
        if adapter.is_valid(row):
            return adapter
    raise NoValidAdapter()


def read(path: str, adapter: Adapter) -> Iterable[Transaction]:
    for row in CsvReader().read(path=path):
        try:
            yield adapter.transform(row)
        except Exception:
            print('error row')