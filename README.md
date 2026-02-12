# Music Program

A Python project with an API and GUI to create any song using notes and music theory.

## Features
- REST API (FastAPI) for music generation
- GUI (Tkinter) for interactive song creation
- Core modules for music theory (notes, scales, chords, song generation)

## Requirements
- Python 3.8+
- FastAPI
- uvicorn
- Tkinter (standard library)
- numpy

## Setup
1. Install dependencies:
   ```sh
   pip install fastapi uvicorn numpy
   ```
2. Run the API:
   ```sh
   uvicorn api:app --reload
   ```
3. Run the GUI:
   ```sh
   python gui.py
   ```

## Usage
- Use the GUI to compose and generate songs interactively.
- Use the REST API to generate songs programmatically.

## Notes
- This is a starting template. Expand music theory modules for advanced features.
