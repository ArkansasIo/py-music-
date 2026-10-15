from __future__ import annotations
import argparse, json
from pathlib import Path
from .composer import SongGenerator
from .midi import export_midi
from .audio import Synth

def main(argv=None):
    p=argparse.ArgumentParser(prog='py-music'); sub=p.add_subparsers(dest='command',required=True)
    g=sub.add_parser('generate'); g.add_argument('--title',default='Generated Song'); g.add_argument('--key',default='C'); g.add_argument('--scale',default='major'); g.add_argument('--bars',type=int,default=8); g.add_argument('--midi'); g.add_argument('--wav')
    args=p.parse_args(argv)
    if args.command=='generate':
        song=SongGenerator().song(args.title,args.key,args.scale,args.bars)
        if args.midi: export_midi(song,args.midi)
        if args.wav: Synth().render(song,args.wav)
        if not args.midi and not args.wav: print(json.dumps(song.to_dict(),indent=2))
if __name__=='__main__': main()
