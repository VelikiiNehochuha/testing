import csv
from typing import Iterable, Dict, Any

class CsvReader:
    def read(self, path: str) -> Iterable[Dict[str, Any]]:
        with open(path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                yield row