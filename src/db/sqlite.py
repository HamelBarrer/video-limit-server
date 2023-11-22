import sqlite3

conn = sqlite3.connect('video.db')

with conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS records (
            record_id integer primary key autoincrement,
            name text not null,
            location text not null,
            created_at timestamp not null default (datetime('now'))
        )
    ''')
