from __future__ import annotations
from pathlib import Path
from ..models import Song, Track, NoteEvent

def export_midi(song:Song,path:str|Path,ticks_per_beat:int=480)->None:
    try:
        import mido
    except ImportError as e: raise RuntimeError("Install mido to use MIDI export") from e
    mid=mido.MidiFile(ticks_per_beat=ticks_per_beat)
    tempo=mido.bpm2tempo(song.tempo)
    for track in song.tracks:
        mt=mido.MidiTrack(); mid.tracks.append(mt); mt.append(mido.MetaMessage('track_name',name=track.name,time=0)); mt.append(mido.MetaMessage('set_tempo',tempo=tempo,time=0))
        events=[]
        for n in track.notes: events += [(n.start,'on',n),(n.end,'off',n)]
        events.sort(key=lambda x:(x[0],0 if x[1]=='off' else 1,x[2].pitch)); last=0
        for at,kind,n in events:
            delta=max(0,round((at-last)*ticks_per_beat)); last=at
            mt.append(mido.Message('note_on' if kind=='on' else 'note_off',note=n.pitch,velocity=n.velocity if kind=='on' else 0,channel=track.channel,time=delta))
    mid.save(str(path))

def import_midi(path:str|Path)->Song:
    try: import mido
    except ImportError as e: raise RuntimeError("Install mido to use MIDI import") from e
    mid=mido.MidiFile(str(path)); tempo=120; song=Song(Path(path).stem,tempo=tempo)
    for i,mt in enumerate(mid.tracks):
        track=Track(f"Track {i}",channel=i%16); pending={}; clock=0.0
        for msg in mt:
            clock += msg.time/mid.ticks_per_beat
            if msg.type=='set_tempo': tempo=mido.tempo2bpm(msg.tempo); song.tempo=tempo
            elif msg.type=='note_on' and msg.velocity>0: pending[(msg.channel,msg.note)]=(clock,msg.velocity)
            elif msg.type in ('note_off','note_on') and msg.velocity==0 or msg.type=='note_off':
                key=(msg.channel,msg.note)
                if key in pending:
                    start,vel=pending.pop(key); track.add(NoteEvent(msg.note,start,max(.001,clock-start),vel,msg.channel))
        track.sort(); song.add_track(track)
    return song
