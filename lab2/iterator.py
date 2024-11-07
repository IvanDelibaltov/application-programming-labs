import csv

class PigsIterator:



    def __init__(self, path_to_csv: str):
        self.path_to_csv = path_to_csv

    def __iter__(self):

        self.file = open(self.path_to_csv, 'r')
        self.csvreader = csv.reader(self.file)
        return self

    def __next__(self):

        try:
            return next(self.csvreader)
        except StopIteration:
            self.file.close()
            raise StopIteration