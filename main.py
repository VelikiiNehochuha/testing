from sqlite3 import adapt
from readers.auto_reader import AutoReader, auto_select_adapter, read
from writers.writer import Writer
from writers.csv_writer import CsvWriter


class Ctrl:
    def __init__(self, get_adapter: AutoReader, writer: Writer):
        self.get_adapter = get_adapter
        self.writer = writer
        self.items = []

    def read(self, path: str) -> None:
        adapter = self.get_adapter(path)
        items = [item for item in read(path, adapter)]
        self.items.extend(items)

    def write(self):
        self.writer.write(self.items)


def main():
    ctrl = Ctrl(get_adapter=auto_select_adapter, writer=CsvWriter('data/result.csv'))
    ctrl.read('data/bank1.csv')
    ctrl.read('data/bank2.csv')
    ctrl.read('data/bank3.csv')
    ctrl.write()


if __name__ == '__main__':
    main()