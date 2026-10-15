"""Py-Music package: music theory, composition, MIDI, audio and persistence."""
from .models import NoteEvent, Track, Song
from .theory import NOTES, get_scale, get_chord, note_to_freq
from .composer import SongGenerator

__version__ = "2.0.0"
__all__ = ["NoteEvent", "Track", "Song", "SongGenerator", "NOTES", "get_scale", "get_chord", "note_to_freq"]
