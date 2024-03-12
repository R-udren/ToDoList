import sqlite3

class DataBaseManager:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

    def create_table(self, table_name: str, columns: list):
        columns = ', '.join(columns)
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')
        self.db.commit()

    def add_record(self, table_name: str, values: list):
        placeholders = ', '.join(['?' for _ in values])
        self.cursor.execute(f'INSERT INTO {table_name} VALUES ({placeholders})', values)
        self.db.commit()

    def get_record(self, table_name: str, column_name: str, value: str):
        self.cursor.execute(f'SELECT * FROM {table_name} WHERE {column_name} = ?', (value,))
        return self.cursor.fetchall()

    def close(self):
        self.db.close()