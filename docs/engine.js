(() => {
  'use strict';
  const NS = window.PyMusic = window.PyMusic || {};
  const NOTE_NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];
  const SCALES = {
    major:[0,2,4,5,7,9,11], natural_minor:[0,2,3,5,7,8,10], dorian:[0,2,3,5,7,9,10],
    phrygian:[0,1,3,5,7,8,10], lydian:[0,2,4,6,7,9,11], mixolydian:[0,2,4,5,7,9,10],
    locrian:[0,1,3,5,6,8,10], harmonic_minor:[0,2,3,5,7,8,11], melodic_minor:[0,2,3,5,7,9,11]
  };
  const CHORDS = {
    major:[0,4,7], minor:[0,3,7], diminished:[0,3,6], augmented:[0,4,8],
    maj7:[0,4,7,11], min7:[0,3,7,10], dom7:[0,4,7,10], dim7:[0,3,6,9], sus2:[0,2,7], sus4:[0,5,7]
  };
  const midiToFreq = m => 440 * Math.pow(2,(m-69)/12);
  const pc = n => ((n%12)+12)%12;
  const noteName = m => NOTE_NAMES[pc(m)];
  const midiName = m => `${noteName(m)}${Math.floor(m/12)-1}`;
  const durationFor = (bpm,beats) => 60/bpm*beats;
  NS.NOTE_NAMES=NOTE_NAMES; NS.SCALES=SCALES; NS.CHORDS=CHORDS; NS.midiToFreq=midiToFreq; NS.midiName=midiName;
  NS.scaleNotes=(root,scale)=>SCALES[scale].map(i=>pc(root+i));
  NS.chordNotes=(root,type)=>CHORDS[type].map(i=>pc(root+i));
  NS.makeMelody=(root,scale,bars=4,stepsPerBar=4,seed=17)=>{
    let s=seed>>>0, next=()=>{s=(1664525*s+1013904223)>>>0;return s/4294967296;};
    const pattern=SCALES[scale], out=[];
    for(let i=0;i<bars*stepsPerBar;i++){
      if(next()<.18){out.push(null);continue;}
      const degree=pattern[Math.floor(next()*pattern.length)];
      out.push(root+60+degree+(next()<.22?12:0));
    }
    return out;
  };
  NS.renderWav=(sequence,bpm,waveform,volume,master)=>{
    const sampleRate=44100, beat=60/bpm, total=Math.ceil(sequence.length*beat*sampleRate+.5*sampleRate);
    const samples=new Float32Array(total);
    const osc=(phase,type)=>type==='square'?(phase<Math.PI?1:-1):type==='sawtooth'?(phase/Math.PI-1):type==='triangle'?(2*Math.abs(2*(phase/(2*Math.PI)-Math.floor(phase/(2*Math.PI)+.5)))-1):Math.sin(phase);
    sequence.forEach((m,i)=>{if(m===null)return; const start=Math.floor(i*beat*sampleRate),len=Math.floor(beat*.9*sampleRate),freq=midiToFreq(m);for(let j=0;j<len&&start+j<samples.length;j++){const t=j/sampleRate,env=Math.min(1,j/(sampleRate*.008))*Math.max(0,1-j/Math.max(1,len));samples[start+j]+=osc(2*Math.PI*freq*t,waveform)*volume*env;}});
    const buf=new ArrayBuffer(44+samples.length*2),v=new DataView(buf),write=(o,s)=>[...s].forEach((c,i)=>v.setUint8(o+i,c.charCodeAt(0)));
    write(0,'RIFF');v.setUint32(4,36+samples.length*2,true);write(8,'WAVE');write(12,'fmt ');v.setUint32(16,16,true);v.setUint16(20,1,true);v.setUint16(22,1,true);v.setUint32(24,sampleRate,true);v.setUint32(28,sampleRate*2,true);v.setUint16(32,2,true);v.setUint16(34,16,true);write(36,'data');v.setUint32(40,samples.length*2,true);samples.forEach((x,i)=>v.setInt16(44+i*2,Math.max(-1,Math.min(1,x*master))*32767,true));return buf;
  };
  NS.download=(blob,name)=>{const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),1000);};
})();
