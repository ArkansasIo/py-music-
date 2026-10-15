(() => {
'use strict';
const P=window.PyMusic||{};
P.DAW=P.DAW||{};
P.DAW.createProject=()=>({version:1,tempo:120,timeSignature:[4,4],length:128,tracks:[]});
P.DAW.generateDrums=(bars=4)=>{const a=[];for(let s=0;s<bars*16;s++){if(s%4===0)a.push({step:s,note:36,velocity:.9});if(s%2===0)a.push({step:s,note:42,velocity:.45});if(s%8===4)a.push({step:s,note:38,velocity:.8});}return a};
P.DAW.generateBass=(root=0,bars=4)=>{const a=[];for(let s=0;s<bars*16;s+=4)a.push({step:s,note:36+root+(s%16===8?7:0),velocity:.75});return a};
P.DAW.makeAutomation=(length=128)=>Array.from({length},(_,i)=>({step:i,value:.5+.35*Math.sin(i/12)}));
P.DAW.adsr=(ctx,node,gain,when,duration,attack=.01,decay=.08,sustain=.65,release=.12)=>{gain.gain.setValueAtTime(.0001,when);gain.gain.linearRampToValueAtTime(1,when+attack);gain.gain.linearRampToValueAtTime(sustain,when+attack+decay);gain.gain.setValueAtTime(sustain,when+Math.max(attack+decay,duration-release));gain.gain.linearRampToValueAtTime(.0001,when+duration);node.start(when);node.stop(when+duration+.02)};
P.DAW.toMidi=(notes,tempo=120)=>{const ppq=480,beat=60/tempo,events=[];notes.forEach(n=>events.push({t:Math.round(n.step*ppq/4),type:0,n:n.note,v:Math.round((n.velocity??.8)*127)},{t:Math.round((n.step+1)*ppq/4),type:1,n:n.note,v:0}));events.sort((a,b)=>a.t-b.t);const bytes=[77,84,104,100,0,0,0,6,0,0,0,1,1,224,77,84,114,107,0,0,0,0];const varint=x=>{let b=[x&127];while(x>>=7)b.unshift((x&127)|128);return b};let last=0;for(const e of events){bytes.push(...varint(e.t-last),144|e.type,e.n,e.v);last=e.t}bytes.push(0,255,47,0);const len=bytes.length-22;bytes[18]=(len>>>24)&255;bytes[19]=(len>>>16)&255;bytes[20]=(len>>>8)&255;bytes[21]=len&255;return new Uint8Array(bytes)};
window.PyMusic=P;
})();
