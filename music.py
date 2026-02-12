import numpy as np
import random
import string

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
SCALES = {
    'major': [2, 2, 1, 2, 2, 2, 1],
    'minor': [2, 1, 2, 2, 1, 2, 2]
}

# Note durations in quarter notes (1 = quarter, 0.5 = eighth, etc.)
DURATIONS = [1, 0.5, 2, 0.25]  # quarter, eighth, half, sixteenth
DURATION_NAMES = {1: 'quarter', 0.5: 'eighth', 2: 'half', 0.25: 'sixteenth'}

# Dynamics
DYNAMICS = ['pp', 'p', 'mp', 'mf', 'f', 'ff']

# Clefs
CLEFS = ['treble', 'bass']

# Note frequencies for A4 = 440Hz
NOTE_FREQS = {
    'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13, 'E': 329.63, 'F': 349.23,
    'F#': 369.99, 'G': 392.00, 'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
}

# Simple lyric templates
LYRIC_TEMPLATES = [
    "Oh {word}, you make me {word2}",
    "{word} in the {word2}, all day long",
    "Sing with {word}, dance with {word2}"
]

# Generate random words for lyrics
WORDS = ["love", "sky", "dream", "light", "night", "heart", "song", "fire", "rain", "star"]

def get_scale(key: str, scale: str):
    """Return the notes in the given key and scale."""
    if key not in NOTES or scale not in SCALES:
        return []
    intervals = SCALES[scale]
    idx = NOTES.index(key)
    scale_notes = [key]
    for step in intervals:
        idx = (idx + step) % 12
        scale_notes.append(NOTES[idx])
    return scale_notes

def generate_lyrics(length: int):
    lines = []
    for _ in range(length):
        template = random.choice(LYRIC_TEMPLATES)
        word = random.choice(WORDS)
        word2 = random.choice(WORDS)
        lines.append(template.format(word=word, word2=word2))
    return '\n'.join(lines)

def generate_song(title: str, key: str, scale: str, length: int, clef: str = 'treble', with_lyrics: bool = True):
    """
    Generate a song as a list of note dictionaries with pitch, duration, and dynamics.
    Each note: {'note': str, 'duration': float, 'dynamic': str, 'clef': str, 'frequency': float}
    Returns: {'notes': [...], 'lyrics': str}
    """
    scale_notes = get_scale(key, scale)
    if not scale_notes:
        return {'notes': [], 'lyrics': ''}
    song = []
    for _ in range(length * 4):
        note = random.choice(scale_notes)
        duration = random.choice(DURATIONS)
        dynamic = random.choice(DYNAMICS)
        freq = NOTE_FREQS[note]
        song.append({
            'note': note,
            'duration': duration,
            'duration_name': DURATION_NAMES[duration],
            'dynamic': dynamic,
            'clef': clef,
            'frequency': freq
        })
    lyrics = generate_lyrics(length) if with_lyrics else ''
    return {'notes': song, 'lyrics': lyrics}
