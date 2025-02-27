import sqlite3
from flask import g

class Database:
    def __init__(self, db_path="./src/lib/dev.db"):
        self.db_path = db_path

    def get_connection(self):
        if "db" not in g:
            g.db = sqlite3.connect(self.db_path)
            g.db.row_factory = sqlite3.Row
        return g.db 

    def close_connection(self):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db(self):
        db = self.get_connection()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()
