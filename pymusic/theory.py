from __future__ import annotations
import math
NOTES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
NOTE_TO_INT={n:i for i,n in enumerate(NOTES)}
ALIASES={"Db":"C#","Eb":"D#","Gb":"F#","Ab":"G#","Bb":"A#"}
SCALE_PATTERNS={"major":[2,2,1,2,2,2,1],"natural_minor":[2,1,2,2,1,2,2],"harmonic_minor":[2,1,2,2,1,3,1],"melodic_minor":[2,1,2,2,2,2,1],"dorian":[2,1,2,2,2,1,2],"phrygian":[1,2,2,2,1,2,2],"lydian":[2,2,2,1,2,2,1],"mixolydian":[2,2,1,2,2,1,2],"locrian":[1,2,2,1,2,2,2]}
CHORDS={"major":[0,4,7],"minor":[0,3,7],"diminished":[0,3,6],"augmented":[0,4,8],"maj7":[0,4,7,11],"min7":[0,3,7,10],"dom7":[0,4,7,10],"dim7":[0,3,6,9],"sus2":[0,2,7],"sus4":[0,5,7]}
def normalize(note:str)->str:
    note=ALIASES.get(note,note)
    if note not in NOTE_TO_INT: raise ValueError(f"Unknown note: {note}")
    return note
def midi_to_freq(midi:int, a4:float=440.0)->float: return a4*2**((midi-69)/12)
def note_to_midi(note:str, octave:int)->int: return NOTE_TO_INT[normalize(note)]+12*(octave+1)
def note_to_freq(note:str, octave:int, a4:float=440.0)->float: return midi_to_freq(note_to_midi(note,octave),a4)
def freq_to_midi(freq:float,a4:float=440.0)->int: return round(69+12*math.log2(freq/a4))
def freq_to_note(freq:float,a4:float=440.0)->tuple[str,int]:
    midi=freq_to_midi(freq,a4); return NOTES[midi%12], midi//12-1
def transpose(note:str,semitones:int)->str: return NOTES[(NOTE_TO_INT[normalize(note)]+semitones)%12]
def interval(a:str,b:str)->int: return (NOTE_TO_INT[normalize(b)]-NOTE_TO_INT[normalize(a)])%12
def get_scale(root:str,pattern:str="major")->list[str]:
    root=normalize(root)
    if pattern not in SCALE_PATTERNS: raise ValueError(f"Unknown scale: {pattern}")
    idx=NOTE_TO_INT[root]; out=[root]
    for step in SCALE_PATTERNS[pattern]: idx=(idx+step)%12; out.append(NOTES[idx])
    return out
def get_chord(root:str,chord_type:str="major")->list[str]:
    root=normalize(root)
    if chord_type not in CHORDS: raise ValueError(f"Unknown chord: {chord_type}")
    i=NOTE_TO_INT[root]; return [NOTES[(i+x)%12] for x in CHORDS[chord_type]]
def roman_progression(root:str,scale:str="major",degrees=(1,5,6,4),chord_type="major")->list[list[str]]:
    notes=get_scale(root,scale)[:-1]; return [get_chord(notes[d-1],chord_type) for d in degrees]
def harmonics(freq:float,n:int=8)->list[float]: return [freq*i for i in range(1,n+1)]
