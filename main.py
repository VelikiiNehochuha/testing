from readers.auto_reader import AutoReader, auto_select_reader
from writers.writer import Writer
from writers.csv_writer import CsvWriter


class Ctrl:
    def __init__(self, get_reader: AutoReader, writer: Writer):
        self.get_reader = get_reader
        self.writer = writer
        self.items = []

    def read(self, path: str) -> None:
        reader = self.get_reader(path)
        items = reader.read(path)
        self.items.extend(items)

    def write(self):
        self.writer.write(self.items)


def main():
    ctrl = Ctrl(get_reader=auto_select_reader, writer=CsvWriter('data/result.csv'))
    ctrl.read('data/bank1.csv')
    ctrl.read('data/bank2.csv')
    ctrl.read('data/bank3.csv')
    ctrl.write()


if __name__ == '__main__':
    main()