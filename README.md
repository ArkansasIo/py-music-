# Music Program

A modular Python music creation program with:
- Song and lyric generation
- Music theory and multi-track support
- Virtual keyboard, audio playback, and oscilloscope
- SoundFont (real instrument) playback
- Database for songs
- MIDI import/export
- Professional folder structure

## Project Structure

- core/ — music theory, types, multi-track
- audio/ — playback, synthesis, soundfont
- ui/ — GUI, panels, widgets
- data/ — database, persistence
- tests/ — test cases
- samples/, soundfonts/ — user assets

## How to Run

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Launch the GUI:
   ```sh
   python ui/main.py
   ```
3. (Optional) Use your own .sf2 SoundFont for realistic playback.

## Features
- Generate songs and lyrics using music theory
- Multi-track editor for multiple instruments
- Play songs with real instrument sounds (SoundFont)
- Save/load songs to/from a database
- MIDI import/export
- Oscilloscope visualization
- Control panel: volume, tempo, play mode, mute, stop

## Requirements
- Python 3.8+
- numpy, sounddevice, matplotlib, mido, pyfluidsynth, tkinter, fastapi, uvicorn

## License
Open source. See LICENSE file.
