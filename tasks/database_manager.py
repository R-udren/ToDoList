import sqlite3

class DatabaseManager:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

    def create_task_table(self, table_name: str, columns: list):
        columns.insert(0, 'user_id TEXT')
        columns.append('FOREIGN KEY(user_id) REFERENCES users(id)')
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

    def read_records(self, table_name: str, user_id : str):
        self.cursor.execute(f'SELECT * FROM {table_name} WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()

    def clear_table(self, table_name: str, user_id : str):
        self.cursor.execute(f'DELETE FROM {table_name} WHERE user_id = ?', (user_id,))
        self.db.commit()


    ## User table functions
        
    def create_user_table(self, table_name: str, columns: list):
        columns.insert(0, 'id TEXT PRIMARY KEY')
        columns = ', '.join(columns)
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')
        self.db.commit()

    def username_exists(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone() is not None
    
    def email_exists(self, email):
        self.cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        return self.cursor.fetchone() is not None
    
    def add_user(self, table_name: str, user_id, username, email, hashed_password):
        self.cursor.execute(f'INSERT INTO {table_name} VALUES (?, ?, ?, ?)', (user_id, username, email, hashed_password))
        self.db.commit()

    def close(self):
        self.db.close()