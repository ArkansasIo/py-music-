from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass(frozen=True, slots=True)
class NoteEvent:
    pitch: int
    start: float
    duration: float
    velocity: int = 90
    channel: int = 0
    lyric: str | None = None
    def __post_init__(self):
        if not 0 <= self.pitch <= 127: raise ValueError("pitch must be 0..127")
        if self.start < 0 or self.duration <= 0: raise ValueError("invalid note timing")
        if not 0 <= self.velocity <= 127: raise ValueError("velocity must be 0..127")
        if not 0 <= self.channel <= 15: raise ValueError("channel must be 0..15")
    @property
    def end(self) -> float: return self.start + self.duration
    def to_dict(self) -> dict[str, Any]: return asdict(self)

@dataclass(slots=True)
class Track:
    name: str = "Track"
    program: int = 0
    channel: int = 0
    volume: float = 1.0
    pan: float = 0.0
    muted: bool = False
    notes: list[NoteEvent] = field(default_factory=list)
    def add(self, note: NoteEvent) -> None: self.notes.append(note)
    def sort(self) -> None: self.notes.sort(key=lambda n: (n.start, n.pitch))
    @property
    def duration(self) -> float: return max((n.end for n in self.notes), default=0.0)

@dataclass(slots=True)
class Song:
    title: str = "Untitled"
    tempo: float = 120.0
    time_signature: tuple[int, int] = (4, 4)
    key: str = "C"
    scale: str = "major"
    tracks: list[Track] = field(default_factory=list)
    lyrics: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    def add_track(self, track: Track) -> None: self.tracks.append(track)
    @property
    def duration(self) -> float: return max((t.duration for t in self.tracks), default=0.0)
    def to_dict(self) -> dict[str, Any]:
        return {"title": self.title, "tempo": self.tempo, "time_signature": list(self.time_signature), "key": self.key, "scale": self.scale,
                "tracks": [{"name":t.name,"program":t.program,"channel":t.channel,"volume":t.volume,"pan":t.pan,"muted":t.muted,"notes":[n.to_dict() for n in t.notes]} for t in self.tracks],
                "lyrics": self.lyrics, "metadata": self.metadata}
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Song":
        song = cls(data.get("title","Untitled"), float(data.get("tempo",120)), tuple(data.get("time_signature",[4,4])), data.get("key","C"), data.get("scale","major"), lyrics=data.get("lyrics",[]), metadata=data.get("metadata",{}))
        for td in data.get("tracks",[]):
            t=Track(td.get("name","Track"),int(td.get("program",0)),int(td.get("channel",0)),float(td.get("volume",1)),float(td.get("pan",0)),bool(td.get("muted",False)))
            t.notes=[NoteEvent(**n) for n in td.get("notes",[])]; song.add_track(t)
        return song
