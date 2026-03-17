import sqlite3

conn = sqlite3.connect('eventscheduler.db')
conn.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT,
        email TEXT,
        password_hash TEXT,
        created_at TEXT,
        updated_at TEXT
    );
    CREATE TABLE IF NOT EXISTS events (
        id TEXT PRIMARY KEY,
        tenant_id TEXT,
        event_type TEXT,
        payload TEXT,
        idempotency_key TEXT,
        created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS accounts (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        created_at TEXT,
        updated_at TEXT
    );
    CREATE TABLE IF NOT EXISTS payments (
        id TEXT PRIMARY KEY,
        account_id TEXT,
        amount TEXT,
        made_at TEXT
    );
    CREATE TABLE IF NOT EXISTS deliveries (
        id TEXT PRIMARY KEY,
        status TEXT
    );
''')
conn.close()
print('Tables created.')
