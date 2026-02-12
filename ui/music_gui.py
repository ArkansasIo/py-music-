import tkinter as tk
from tkinter import ttk, messagebox
from music import generate_song, generate_any_song
from db import init_db, save_song, get_songs
import threading
import sounddevice as sd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from theory import Track

KEYBOARD_NOTES = [
    {'note': 'C', 'frequency': 261.63},
    {'note': 'D', 'frequency': 293.66},
    {'note': 'E', 'frequency': 329.63},
    {'note': 'F', 'frequency': 349.23},
    {'note': 'G', 'frequency': 392.00},
    {'note': 'A', 'frequency': 440.00},
    {'note': 'B', 'frequency': 493.88},
]

class MusicGUI(tk.Toplevel):
    # ...existing MusicGUI code from previous gui.py...
    pass
