import csv

class CSVManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path, 'r') as file:
            reader = csv.reader(file)
            return list(reader)

    def write(self, data):
        with open(self.file_path, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(data)