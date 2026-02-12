import math

# Note names and mapping
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_TO_INT = {n: i for i, n in enumerate(NOTES)}
INT_TO_NOTE = {i: n for i, n in enumerate(NOTES)}

# Frequency math (A4 = 440Hz)
def note_to_freq(note, octave):
    n = NOTE_TO_INT[note]
    midi = n + 12 * (octave + 1)
    return 440.0 * 2 ** ((midi - 69) / 12)

def freq_to_note(freq):
    midi = round(12 * math.log2(freq / 440.0) + 69)
    note = INT_TO_NOTE[midi % 12]
    octave = midi // 12 - 1
    return note, octave

# Intervals
def interval(note1, note2):
    return (NOTE_TO_INT[note2] - NOTE_TO_INT[note1]) % 12

# Transpose note by interval
def transpose(note, interval):
    idx = (NOTE_TO_INT[note] + interval) % 12
    return INT_TO_NOTE[idx]

# Scales and modes
SCALE_PATTERNS = {
    'major':        [2, 2, 1, 2, 2, 2, 1],
    'natural_minor':[2, 1, 2, 2, 1, 2, 2],
    'harmonic_minor':[2, 1, 2, 2, 1, 3, 1],
    'melodic_minor':[2, 1, 2, 2, 2, 2, 1],
    'dorian':       [2, 1, 2, 2, 2, 1, 2],
    'phrygian':     [1, 2, 2, 2, 1, 2, 2],
    'lydian':       [2, 2, 2, 1, 2, 2, 1],
    'mixolydian':   [2, 2, 1, 2, 2, 1, 2],
    'locrian':      [1, 2, 2, 1, 2, 2, 2],
}

def get_scale(root, pattern):
    idx = NOTE_TO_INT[root]
    notes = [root]
    for step in SCALE_PATTERNS[pattern]:
        idx = (idx + step) % 12
        notes.append(INT_TO_NOTE[idx])
    return notes

# Chord formulas
CHORDS = {
    'major':      [0, 4, 7],
    'minor':      [0, 3, 7],
    'diminished': [0, 3, 6],
    'augmented':  [0, 4, 8],
    'maj7':       [0, 4, 7, 11],
    'min7':       [0, 3, 7, 10],
    'dom7':       [0, 4, 7, 10],
    'dim7':       [0, 3, 6, 9],
    'sus2':       [0, 2, 7],
    'sus4':       [0, 5, 7],
}

def get_chord(root, chord_type):
    idx = NOTE_TO_INT[root]
    return [INT_TO_NOTE[(idx + i) % 12] for i in CHORDS[chord_type]]

# Invert chord
def invert_chord(chord, n=1):
    return chord[n:] + chord[:n]

# Key signatures (sharps)
KEY_SIGNATURES = {
    'C': [], 'G': ['F#'], 'D': ['F#', 'C#'], 'A': ['F#', 'C#', 'G#'],
    'E': ['F#', 'C#', 'G#', 'D#'], 'B': ['F#', 'C#', 'G#', 'D#', 'A#'],
    'F#': ['F#', 'C#', 'G#', 'D#', 'A#', 'E#'], 'C#': ['F#', 'C#', 'G#', 'D#', 'A#', 'E#', 'B#'],
}

# Math for harmonics
def harmonics(freq, n=5):
    return [freq * (i+1) for i in range(n)]

# Example: get_scale('C', 'major'), get_chord('C', 'maj7'), note_to_freq('A', 4)

class Note:
    def __init__(self, name, octave, duration=1.0, dynamic='mf'):
        self.name = name
        self.octave = octave
        self.duration = duration
        self.dynamic = dynamic
        self.frequency = note_to_freq(name, octave)
    def __repr__(self):
        return f"{self.name}{self.octave}({self.duration}, {self.dynamic})"

class Chord:
    def __init__(self, root, chord_type):
        self.root = root
        self.chord_type = chord_type
        self.notes = get_chord(root, chord_type)
    def __repr__(self):
        return f"{self.root} {self.chord_type}: {self.notes}"

class Scale:
    def __init__(self, root, pattern):
        self.root = root
        self.pattern = pattern
        self.notes = get_scale(root, pattern)
    def __repr__(self):
        return f"{self.root} {self.pattern}: {self.notes}"

class Song:
    def __init__(self, title, key, scale, melody, chords, lyrics):
        self.title = title
        self.key = key
        self.scale = scale
        self.melody = melody
        self.chords = chords
        self.lyrics = lyrics
    def __repr__(self):
        return f"Song: {self.title}\nKey: {self.key} {self.scale}\nMelody: {self.melody}\nChords: {self.chords}\nLyrics:\n{self.lyrics}"

class Track:
    def __init__(self, name="Track", instrument="Piano"):
        self.name = name
        self.instrument = instrument
        self.notes = []
    def add_note(self, note):
        self.notes.append(note)
    def __repr__(self):
        return f"{self.name} ({self.instrument}): {self.notes}"

class MultiTrackSong:
    def __init__(self, title, key, scale):
        self.title = title
        self.key = key
        self.scale = scale
        self.tracks = []
    def add_track(self, track):
        self.tracks.append(track)
    def __repr__(self):
        return f"MultiTrackSong: {self.title}\nKey: {self.key} {self.scale}\nTracks: {self.tracks}"

# Utility functions for music logic
def invert_melody(melody):
    if not melody:
        return []
    first = melody[0].octave * 12 + NOTE_TO_INT[melody[0].name]
    return [Note(n.name, n.octave - ((n.octave * 12 + NOTE_TO_INT[n.name]) - first) // 12, n.duration, n.dynamic) for n in melody]

def retrograde_melody(melody):
    return list(reversed(melody))
