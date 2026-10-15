from __future__ import annotations
import json, sqlite3
from pathlib import Path
from ..models import Song
class SongRepository:
    def __init__(self,path="songs.sqlite3"):
        self.path=Path(path); self._init()
    def _connect(self): return sqlite3.connect(self.path)
    def _init(self):
        with self._connect() as c: c.execute("CREATE TABLE IF NOT EXISTS songs(id INTEGER PRIMARY KEY,title TEXT NOT NULL,tempo REAL NOT NULL,key TEXT,scale TEXT,data TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP,updated_at TEXT DEFAULT CURRENT_TIMESTAMP)")
    def save(self,song:Song, song_id:int|None=None)->int:
        payload=json.dumps(song.to_dict())
        with self._connect() as c:
            if song_id is None:
                cur=c.execute("INSERT INTO songs(title,tempo,key,scale,data) VALUES(?,?,?,?,?)",(song.title,song.tempo,song.key,song.scale,payload)); return int(cur.lastrowid)
            c.execute("UPDATE songs SET title=?,tempo=?,key=?,scale=?,data=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",(song.title,song.tempo,song.key,song.scale,payload,song_id)); return song_id
    def get(self,song_id:int)->Song|None:
        with self._connect() as c: row=c.execute("SELECT data FROM songs WHERE id=?",(song_id,)).fetchone()
        return Song.from_dict(json.loads(row[0])) if row else None
    def list(self)->list[tuple[int,str,float]]:
        with self._connect() as c: return c.execute("SELECT id,title,tempo FROM songs ORDER BY updated_at DESC").fetchall()
    def delete(self,song_id:int)->None:
        with self._connect() as c:c.execute("DELETE FROM songs WHERE id=?",(song_id,))
