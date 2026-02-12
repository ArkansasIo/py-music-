import numpy as np
import random
from theory import get_scale, get_chord, NOTES
import mido
from mido import MidiFile, MidiTrack, Message
import fluidsynth

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

# Keyboard note mapping (piano keys, 88-key standard)
KEYBOARD_NOTES = []
A0_FREQ = 27.5
for i in range(88):
    freq = A0_FREQ * (2 ** (i / 12))
    # Note name calculation
    note_name = NOTES[i % 12] + str((i + 9) // 12)
    KEYBOARD_NOTES.append({'note': note_name, 'frequency': freq})

# MIDI note numbers (0-127)
MIDI_NOTES = [{'note': NOTES[n % 12] + str(n // 12 - 1), 'midi': n, 'frequency': 440.0 * 2 ** ((n - 69) / 12)} for n in range(128)]

# Guitar standard tuning (EADGBE, 6 strings, 12 frets)
GUITAR_STRINGS = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
GUITAR_FRETS = 12
guitar_notes = []
for s, open_note in enumerate(GUITAR_STRINGS):
    base_idx = NOTES.index(open_note[:-1])
    octave = int(open_note[-1])
    for f in range(GUITAR_FRETS + 1):
        note_idx = (base_idx + f) % 12
        note_oct = octave + ((base_idx + f) // 12)
        note_name = NOTES[note_idx] + str(note_oct)
        freq = NOTE_FREQS[NOTES[note_idx]] * (2 ** (note_oct - 4))
        guitar_notes.append({'string': s+1, 'fret': f, 'note': note_name, 'frequency': freq})

# Drum kit (basic mapping)
DRUM_KIT = [
    {'name': 'Kick', 'midi': 36},
    {'name': 'Snare', 'midi': 38},
    {'name': 'Hi-Hat Closed', 'midi': 42},
    {'name': 'Hi-Hat Open', 'midi': 46},
    {'name': 'Tom Low', 'midi': 41},
    {'name': 'Tom Mid', 'midi': 45},
    {'name': 'Tom High', 'midi': 48},
    {'name': 'Crash', 'midi': 49},
    {'name': 'Ride', 'midi': 51}
]

# Advanced lyric generator using templates and random words
GENERIC_WORDS = [
    "love", "sky", "dream", "light", "night", "heart", "song", "fire", "rain", "star",
    "dance", "hope", "shine", "wind", "river", "road", "home", "friend", "memory", "time"
]
GENERIC_VERBS = ["run", "fly", "sing", "cry", "shine", "fall", "rise", "wait", "find", "lose"]
GENERIC_TEMPLATES = [
    "{word1} and {word2}, we {verb1} through the {word3}",
    "In the {word1}, I {verb1} for you",
    "{word1} of {word2}, {verb1} in the {word3}",
    "{word1} will {verb1}, {word2} will {verb2}"
]

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

def generate_lyrics_advanced(length: int):
    lines = []
    for _ in range(length):
        template = random.choice(GENERIC_TEMPLATES)
        word1 = random.choice(GENERIC_WORDS)
        word2 = random.choice(GENERIC_WORDS)
        word3 = random.choice(GENERIC_WORDS)
        verb1 = random.choice(GENERIC_VERBS)
        verb2 = random.choice(GENERIC_VERBS)
        lines.append(template.format(word1=word1, word2=word2, word3=word3, verb1=verb1, verb2=verb2))
    return '\n'.join(lines)

# Algorithm to generate any song (melody, chords, lyrics)
def generate_any_song(title: str, key: str, scale: str, length: int, clef: str = 'treble', with_lyrics: bool = True):
    # Melody: use scale notes
    scale_notes = get_scale(key, scale)
    if not scale_notes:
        return {'notes': [], 'chords': [], 'lyrics': ''}
    melody = []
    chords = []
    for i in range(length * 4):
        note = random.choice(scale_notes)
        duration = random.choice([1, 0.5, 2, 0.25])
        melody.append({'note': note, 'duration': duration, 'clef': clef})
        # Chord progression: I-IV-V or random
        if i % 4 == 0:
            root = scale_notes[0] if i % 8 == 0 else scale_notes[3] if i % 8 == 4 else scale_notes[4]
            chord = get_chord(root, 'major')
            chords.append({'root': root, 'chord': chord})
    lyrics = generate_lyrics_advanced(length) if with_lyrics else ''
    return {'melody': melody, 'chords': chords, 'lyrics': lyrics}

# Generate a song as a list of note dictionaries with pitch, duration, and dynamics.
# Each note: {'note': str, 'duration': float, 'dynamic': str, 'clef': str, 'frequency': float}
# Returns: {'notes': [...], 'lyrics': str}
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

def export_midi(song, filename="output.mid"):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    tempo = mido.bpm2tempo(120)
    track.append(mido.MetaMessage('set_tempo', tempo=tempo))
    for note in song['notes'] if 'notes' in song else song.get('melody', []):
        midi_note = 60 + NOTES.index(note['note'])  # C4 = 60
        duration = int(480 * note['duration'])
        track.append(Message('note_on', note=midi_note, velocity=64, time=0))
        track.append(Message('note_off', note=midi_note, velocity=64, time=duration))
    mid.save(filename)

def import_midi(filename):
    mid = MidiFile(filename)
    notes = []
    for track in mid.tracks:
        time = 0
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append({'note': NOTES[(msg.note - 60) % 12], 'duration': 1, 'velocity': msg.velocity})
    return notes

def play_song_with_soundfont(song, soundfont_path, instrument=0):
    fs = fluidsynth.Synth()
    fs.start(driver="dsound")
    sfid = fs.sfload(soundfont_path)
    fs.program_select(0, sfid, 0, instrument)
    sample_rate = 44100
    notes = song['notes'] if 'notes' in song else song.get('melody', [])
    for note in notes:
        midi_note = 60 + NOTES.index(note['note'])  # C4 = 60
        duration = int(note['duration'] * 1000)  # ms
        fs.noteon(0, midi_note, 100)
        fluidsynth.sleep(duration / 1000)
        fs.noteoff(0, midi_note)
    fs.delete()
