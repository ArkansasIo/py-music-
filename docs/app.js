(() => {
  'use strict';

  const A4 = 440;
  const NOTE_NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];
  const SCALE_PATTERNS = {
    major:[0,2,4,5,7,9,11], natural_minor:[0,2,3,5,7,8,10], dorian:[0,2,3,5,7,9,10],
    phrygian:[0,1,3,5,7,8,10], lydian:[0,2,4,6,7,9,11], mixolydian:[0,2,4,5,7,9,10],
    locrian:[0,1,3,5,6,8,10], harmonic_minor:[0,2,3,5,7,8,11], melodic_minor:[0,2,3,5,7,9,11]
  };
  const CHORD_PATTERNS = {
    major:[0,4,7], minor:[0,3,7], diminished:[0,3,6], augmented:[0,4,8],
    maj7:[0,4,7,11], min7:[0,3,7,10], dom7:[0,4,7,10], dim7:[0,3,6,9], sus2:[0,2,7], sus4:[0,5,7]
  };
  const state = { bpm:120, key:0, scale:'major', steps:16, sequence:Array(16).fill(null), waveform:'sine', volume:0.16, octave:4 };
  let audio = null;

  const $ = id => document.getElementById(id);
  const midiToName = midi => `${NOTE_NAMES[(midi % 12 + 12) % 12]}${Math.floor(midi / 12) - 1}`;
  const midiToFreq = midi => A4 * Math.pow(2, (midi - 69) / 12);
  const nameToPc = name => NOTE_NAMES.indexOf(name.replace('♯','#').replace('♭',''));
  const escapeHtml = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

  function renderTheory() {
    const root = state.key;
    const pattern = SCALE_PATTERNS[state.scale];
    $('scaleOutput').innerHTML = pattern.map(i => `<span class="pill">${NOTE_NAMES[(root+i)%12]}</span>`).join('');
    const chordType = $('chordType').value;
    const chordRoot = Number($('chordRoot').value);
    $('chordOutput').innerHTML = CHORD_PATTERNS[chordType].map(i => `<span class="pill">${NOTE_NAMES[(chordRoot+i)%12]}</span>`).join('');
    $('formulaOutput').textContent = `Scale intervals: ${pattern.join('–')} semitones from root. Chord: ${CHORD_PATTERNS[chordType].join(', ')}.`;
  }

  function renderPiano() {
    const root = state.key;
    const scale = new Set(SCALE_PATTERNS[state.scale]);
    const start = 48, count = 25;
    $('piano').innerHTML = '';
    for (let i=0;i<count;i++) {
      const midi = start+i, pc=midi%12, white=!['C#','D#','F#','G#','A#'].includes(NOTE_NAMES[pc]);
      const key=document.createElement('button');
      key.className='key '+(white?'white':'black')+(scale.has((pc-root+12)%12)?' in-scale':'');
      key.innerHTML=`<span>${NOTE_NAMES[pc]}</span><small>${midi}</small>`;
      key.addEventListener('pointerdown', e => { e.preventDefault(); playNote(midi,0.45); });
      $('piano').appendChild(key);
    }
  }

  function renderSequencer() {
    $('sequencer').innerHTML='';
    state.sequence.forEach((midi,i)=>{
      const cell=document.createElement('button'); cell.className='step '+(midi!==null?'active':'');
      cell.title=`Step ${i+1}`;
      cell.textContent=midi===null?'·':midiToName(midi);
      cell.onclick=()=>{ state.sequence[i]=midi===null ? state.key+60 : null; renderSequencer(); if(state.sequence[i]!=null) playNote(state.sequence[i],0.2); };
      $('sequencer').appendChild(cell);
    });
  }

  function ensureAudio() {
    if (!audio) audio = new (window.AudioContext || window.webkitAudioContext)();
    if (audio.state === 'suspended') audio.resume();
    return audio;
  }

  function playNote(midi, duration=0.5, when=0) {
    const ctx=ensureAudio(), now=ctx.currentTime+when;
    const osc=ctx.createOscillator(), gain=ctx.createGain();
    osc.type=state.waveform; osc.frequency.value=midiToFreq(midi);
    gain.gain.setValueAtTime(0.0001,now); gain.gain.exponentialRampToValueAtTime(state.volume,now+0.012);
    gain.gain.exponentialRampToValueAtTime(0.0001,now+duration);
    osc.connect(gain).connect(ctx.destination); osc.start(now); osc.stop(now+duration+0.03);
  }

  async function playSequence() {
    ensureAudio(); const beat=60/state.bpm;
    state.sequence.forEach((m,i)=>{ if(m!==null) playNote(m,beat*0.82,i*beat); });
    $('status').textContent=`Playing ${state.sequence.filter(Boolean).length} notes at ${state.bpm} BPM.`;
  }

  function renderWav() {
    const notes=state.sequence.filter(n=>n!==null); if(!notes.length){ $('status').textContent='Add notes to the sequencer first.'; return; }
    const sampleRate=44100, beat=60/state.bpm, noteDur=beat*0.82, total=Math.ceil((state.sequence.length*beat+0.2)*sampleRate);
    const samples=new Float32Array(total);
    state.sequence.forEach((m,idx)=>{ if(m===null)return; const start=Math.floor(idx*beat*sampleRate), len=Math.floor(noteDur*sampleRate), freq=midiToFreq(m);
      for(let j=0;j<len && start+j<samples.length;j++){ const t=j/sampleRate, env=Math.min(1,j/(sampleRate*.01))*Math.max(0,1-j/Math.max(1,len)); samples[start+j]+=Math.sin(2*Math.PI*freq*t)*state.volume*env; }
    });
    const buffer=new ArrayBuffer(44+samples.length*2), view=new DataView(buffer);
    const write=(o,s)=>{for(let i=0;i<s.length;i++)view.setUint8(o+i,s.charCodeAt(i));};
    write(0,'RIFF'); view.setUint32(4,36+samples.length*2,true); write(8,'WAVE'); write(12,'fmt '); view.setUint32(16,16,true); view.setUint16(20,1,true); view.setUint16(22,1,true); view.setUint32(24,sampleRate,true); view.setUint32(28,sampleRate*2,true); view.setUint16(32,2,true); view.setUint16(34,16,true); write(36,'data'); view.setUint32(40,samples.length*2,true);
    samples.forEach((v,i)=>view.setInt16(44+i*2,Math.max(-1,Math.min(1,v))*32767,true));
    const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([buffer],{type:'audio/wav'})); a.download='py-music-sequence.wav'; a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),1000); $('status').textContent='WAV rendered and downloaded.';
  }

  function saveProject() {
    const data={version:1,bpm:state.bpm,key:state.key,scale:state.scale,waveform:state.waveform,volume:state.volume,sequence:state.sequence};
    localStorage.setItem('pymusic-project',JSON.stringify(data)); $('status').textContent='Project saved locally.';
  }
  function loadProject() {
    try { const d=JSON.parse(localStorage.getItem('pymusic-project')); if(!d) throw Error(); Object.assign(state,d); syncControls(); renderAll(); $('status').textContent='Project loaded.'; } catch { $('status').textContent='No saved project found.'; }
  }
  function exportJson() {
    const blob=new Blob([JSON.stringify({format:'Py-Music Project',version:1,...state},null,2)],{type:'application/json'});
    const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='py-music-project.json';a.click();
  }

  function syncControls(){ $('bpm').value=state.bpm; $('bpmValue').textContent=state.bpm; $('key').value=NOTE_NAMES[state.key]; $('scale').value=state.scale; $('waveform').value=state.waveform; $('volume').value=Math.round(state.volume*100); $('volumeValue').textContent=Math.round(state.volume*100)+'%'; }
  function renderAll(){ syncControls(); renderTheory(); renderPiano(); renderSequencer(); }

  document.addEventListener('DOMContentLoaded',()=>{
    $('bpm').oninput=e=>{state.bpm=+e.target.value;$('bpmValue').textContent=state.bpm;};
    $('key').onchange=e=>{state.key=nameToPc(e.target.value);renderAll();};
    $('scale').onchange=e=>{state.scale=e.target.value;renderAll();};
    $('waveform').onchange=e=>state.waveform=e.target.value;
    $('volume').oninput=e=>{state.volume=+e.target.value/100;$('volumeValue').textContent=e.target.value+'%';};
    $('chordRoot').onchange=renderTheory; $('chordType').onchange=renderTheory;
    $('play').onclick=playSequence; $('render').onclick=renderWav; $('save').onclick=saveProject; $('load').onclick=loadProject; $('export').onclick=exportJson;
    $('clear').onclick=()=>{state.sequence.fill(null);renderSequencer();$('status').textContent='Sequencer cleared.';};
    $('random').onclick=()=>{const p=SCALE_PATTERNS[state.scale];state.sequence=state.sequence.map(()=>Math.random()<.25?null:state.key+60+p[Math.floor(Math.random()*p.length)]+(Math.random()<.3?12:0));renderSequencer();};
    renderAll();
  });
})();
