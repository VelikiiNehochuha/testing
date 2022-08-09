from transaction import Transaction


class Writer:
    def write(self, transactions: list[Transaction]) -> None:
        ...


class ConsoleWriter:
    def write(self, transactions: list[Transaction]) -> None:
        print(transactions)