import csv

class PigsIterator:
    def __init__(self, path_to_csv: str):
        self.path_to_csv = path_to_csv

    def __iter__(self):
        """Инициализация итератора"""
        self.file = open(self.path_to_csv, 'r')
        self.csvreader = csv.reader(self.file)
        next(self.csvreader)  # Пропускаем заголовок
        return self

    def __next__(self):
        """Возвращает следующий путь к изображению"""
        try:
            return next(self.csvreader)[0]  # Путь к изображению в первом столбце
        except StopIteration:
            self.file.close()
            raise StopIteration