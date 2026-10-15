from __future__ import annotations
import random
from .models import NoteEvent, Track, Song
from .theory import NOTE_TO_INT, get_scale, get_chord, note_to_midi

DURATION_WEIGHTS=[(1.0,.40),(.5,.30),(2.0,.15),(.25,.15)]
DYNAMICS={"pp":35,"p":50,"mp":70,"mf":88,"f":108,"ff":124}
class SongGenerator:
    def __init__(self, seed:int|None=None): self.rng=random.Random(seed)
    def _duration(self):
        x=self.rng.random(); total=0
        for value,weight in DURATION_WEIGHTS:
            total+=weight
            if x<=total:return value
        return 1.0
    def melody(self,key="C",scale="major",bars=8,octave=4,channel=0)->Track:
        notes=get_scale(key,scale)[:-1]; t=Track("Melody",0,channel)
        time=0.0; beats=bars*4
        while time<beats:
            dur=min(self._duration(),beats-time); name=self.rng.choice(notes); pitch=note_to_midi(name,octave+self.rng.choice([-1,0,0,0,1])); vel=self.rng.randint(70,110)
            t.add(NoteEvent(pitch,time,dur,vel,channel)); time+=dur
        return t
    def chords(self,key="C",scale="major",bars=8,channel=1)->Track:
        scale_notes=get_scale(key,scale)[:-1]; t=Track("Chords",0,channel); progression=[0,3,4,0,5,3,4,0]
        for bar in range(bars):
            root=scale_notes[progression[bar%len(progression)]%7]; chord=get_chord(root,"minor" if scale.endswith("minor") else "major")
            for name in chord: t.add(NoteEvent(note_to_midi(name,4),bar*4,4,72,channel))
        return t
    def song(self,title="Generated Song",key="C",scale="major",bars=8,with_chords=True)->Song:
        s=Song(title=title,key=key,scale=scale); s.add_track(self.melody(key,scale,bars))
        if with_chords:s.add_track(self.chords(key,scale,bars)); return s
        return s

def generate_lyrics(length:int,seed:int|None=None)->list[str]:
    rng=random.Random(seed); nouns=["light","night","dream","river","fire","star","home","road","heart","sky"]; verbs=["rise","fall","shine","run","sing","remember","wander","breathe"]
    return [f"{rng.choice(nouns).title()} {rng.choice(verbs)} through the {rng.choice(nouns)}" for _ in range(length)]
