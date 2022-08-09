import csv

from transaction import Transaction


class CsvWriter:
    def __init__(self, path: str) -> None:
        self.path = path

    def write(self, transactions: list[Transaction]) -> None:
        with open(self.path, 'w') as csv_file:
            fields = list(Transaction.__fields__.keys())
            writer = csv.DictWriter(csv_file, fieldnames=fields)
            writer.writeheader()
            for transaction in transactions:
                writer.writerow(
                    {
                        'date': transaction.date,
                        'type': transaction.type.name,
                        'amount_cents': transaction.amount_cents,
                        'to_id': transaction.from_id,
                        'from_id': transaction.from_id,
                    }
                )