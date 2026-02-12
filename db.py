import sqlite3

DB_NAME = 'songs.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        key TEXT,
        scale TEXT,
        clef TEXT,
        notes TEXT,
        lyrics TEXT
    )''')
    conn.commit()
    conn.close()

def save_song(title, key, scale, clef, notes, lyrics):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO songs (title, key, scale, clef, notes, lyrics) VALUES (?, ?, ?, ?, ?, ?)''',
              (title, key, scale, clef, notes, lyrics))
    conn.commit()
    conn.close()

def get_songs():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM songs')
    songs = c.fetchall()
    conn.close()
    return songs
