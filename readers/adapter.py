from typing import Protocol, Dict, Any

from transaction import Transaction


class Adapter(Protocol):

    def is_valid(self, row: Dict[str, Any]) -> bool:
        ...

    def transform(self, row: Dict[str, Any]) -> Transaction:
        ...