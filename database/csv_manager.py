import os

from config import CSV_NAME, CSV_DELIMITER


class CSVManager:
    @staticmethod
    def check_path(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def export_csv(data: list, header: str, csv_name: str = CSV_NAME, path: str = None) -> int:
        if path is None:
            path = os.getcwd()
        if not os.path.exists(path):
            raise FileNotFoundError("Path does not exist!")
        path = os.path.join(path, csv_name)
        row_counter = 0

        with open(path, 'w') as file:
            file.write(header + '\n')
            for row in data:
                file.write(row + '\n')
                row_counter += 1

        if not os.path.exists(path):
            raise FileExistsError("File does not created!")

        return row_counter

    @staticmethod
    def import_csv(header: str, path):
        if not os.path.exists(path):
            raise Exception("File does not exist!")

        with open(path, 'r') as file:
            for line in file:
                if line.startswith(header) and line.endswith('\n'):
                    continue
                yield line.strip().split(CSV_DELIMITER)  # Return a generator
