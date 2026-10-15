# Py-Music

A modular Python music creation toolkit. The existing repository already contains music theory, song generation, GUI/audio prototypes, a database, MIDI support and tests; this revision organizes those capabilities into a reusable `pymusic` package. fileciteturn4file0

## Architecture

- `pymusic/models.py` — typed Song/Track/NoteEvent domain model.
- `pymusic/theory.py` — pitch/frequency conversion, scales, chords, transposition and harmonics.
- `pymusic/composer.py` — deterministic/randomized melody and chord generation.
- `pymusic/midi.py` — MIDI import/export through Mido.
- `pymusic/audio.py` — dependency-light WAV synthesis plus optional sounddevice playback.
- `pymusic/data/repository.py` — SQLite persistence.
- `pymusic/cli.py` — command-line generation workflow.

The legacy top-level modules remain available for compatibility. The new package avoids the previous duplication between `music.py` and `theory.py`, while keeping the original project's core goals of song generation, theory, multitrack support, playback, MIDI and persistence. fileciteturn2file0

## Install

```bash
python -m pip install -e .
# optional complete stack
python -m pip install -e '.[all,test]'
```

## Generate a song

```bash
py-music generate --title "Aurora" --key C --scale major --bars 16 --midi aurora.mid --wav aurora.wav
```

## Python API

```python
from pymusic.composer import SongGenerator
from pymusic.midi import export_midi
from pymusic.audio import Synth

song = SongGenerator(seed=42).song("Demo", "D", "dorian", bars=8)
export_midi(song, "demo.mid")
Synth().render(song, "demo.wav")
```

## Design principles

1. **Data first:** musical events are plain typed objects and can be serialized.
2. **Determinism:** composition can use a seed for reproducible results.
3. **Optional backends:** theory/composition work without audio hardware.
4. **Interchange:** MIDI is the primary interoperable sequence format.
5. **Testability:** algorithms are separated from GUI and hardware concerns.
6. **Extensibility:** additional synthesizers, notation engines, DAW adapters and APIs can be added without changing the core model.

## Planned extension points

- SoundFont renderer and instrument registry.
- MIDI device input/output and clock synchronization.
- Piano-roll and notation editor.
- DSP effects: EQ, compressor, delay, reverb and limiter.
- Audio analysis: RMS, peak, FFT, spectral centroid and tempo estimation.
- Plugin protocol for instruments/effects/exporters.
- FastAPI service and WebSocket live playback control.
- Project file format with versioned migrations.

No copyrighted music is bundled. Users supply their own audio, MIDI and SoundFont assets.
