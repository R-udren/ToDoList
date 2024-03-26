import sqlite3

class DatabaseManager:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

    # Task table functions
    def create_task_table(self, table_name: str, columns: list):
        columns.append('FOREIGN KEY(email) REFERENCES users(email)')
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

    def read_records(self, table_name: str, email : str):
        self.cursor.execute(f'SELECT * FROM {table_name} WHERE email = ?', (email,))
        return self.cursor.fetchall()

    def clear_table(self, table_name: str, email : str):
        self.cursor.execute(f'DELETE FROM {table_name} WHERE email = ?', (email,))
        self.db.commit()

    def delete_table(self, table_name: str):
        self.cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
        self.db.commit()

    # User table functions
    def create_user_table(self, table_name: str, columns: list):
        columns = ', '.join(columns)
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')
        self.db.commit()

    def username_exists(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone() is not None
    
    def email_exists(self, email):
        self.cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        return self.cursor.fetchone() is not None

    def add_user(self, table_name: str, username, email, password):
        self.cursor.execute(f'INSERT INTO {table_name} VALUES (?, ?, ?)', (username, email, password))
        self.db.commit()

    def close(self):
        self.db.close()

    def export_to_csv(self, table_name: str, csv_name: str, email: str):
        self.cursor.execute(f'SELECT * FROM {table_name} WHERE email = ?', (email,))
        with open(f'{csv_name}.csv', 'w') as file:
            for record in self.cursor.fetchall():
                file.write(','.join([str(col) for col in record]) + '\n')
        self.db.commit()
