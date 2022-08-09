from typing import Callable

from readers.bank_one import BankOneReader
from readers.bank_two import BankTwoReader
from readers.bank_three import BankThreeReader
from readers.reader import Reader
from readers.errors import NoValidReader

READER_CLASSES = (
    BankOneReader,
    BankTwoReader,
    BankThreeReader,
)

AutoReader = Callable[[str], Reader]

def auto_select_reader(path: str) -> Reader:
    for reader_class in READER_CLASSES:
        reader = reader_class()
        if reader.is_valid(path):
            return reader
    raise NoValidReader()
