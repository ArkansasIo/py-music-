from __future__ import annotations
import math, struct, wave
from array import array
from pathlib import Path
from ..models import Song
from ..theory import midi_to_freq
class Synth:
    def __init__(self,sample_rate=44100): self.sample_rate=sample_rate
    def render(self,song:Song,path:str|Path,waveform="sine"):
        frames=int((song.duration+.1)*self.sample_rate); data=array('h',[0])*frames
        for track in song.tracks:
            if track.muted: continue
            for n in track.notes:
                start=int(n.start*self.sample_rate); end=min(frames,int(n.end*self.sample_rate)); amp=min(1.0,n.velocity/127)*track.volume*.22
                freq=midi_to_freq(n.pitch)
                for i in range(start,end):
                    t=(i-start)/self.sample_rate; env=min(1,t/.01,(n.duration-t)/.03) if t>=0 else 0
                    if waveform=='square': sample=1.0 if math.sin(2*math.pi*freq*t)>=0 else -1.0
                    elif waveform=='saw': sample=2*((freq*t)%1)-1
                    else: sample=math.sin(2*math.pi*freq*t)
                    value=int(32767*amp*max(0,env)*sample); data[i]=max(-32768,min(32767,data[i]+value))
        with wave.open(str(path),'wb') as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(self.sample_rate); wf.writeframes(data.tobytes())

def play_file(path:str):
    try:
        import sounddevice as sd
        import soundfile as sf
    except ImportError as e: raise RuntimeError("Install sounddevice and soundfile for playback") from e
    data,rate=sf.read(path,dtype='float32'); sd.play(data,rate); sd.wait()
