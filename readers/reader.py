from typing import Protocol

from transaction import Transaction


class Reader(Protocol):

    def is_valid(self, path: str) -> bool:
        ...

    def read(self, path: str) -> list[Transaction]:
        ...