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

class MusicGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Program")
        self.geometry("900x800")
        init_db()
        self.create_menu()
        self.create_toolbar()
        self.create_control_panel()
        self.create_widgets()
        self.create_multitrack_panel()

    def create_menu(self):
        menubar = tk.Menu(self)
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Song", command=self.generate)
        file_menu.add_command(label="Save Song", command=self.save_song)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Show Keyboard", command=self.show_keyboard)
        tools_menu.add_command(label="Show Oscilloscope", command=self.show_oscilloscope)
        tools_menu.add_command(label="Show Saved Songs", command=self.show_songs)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        # Generate menu
        gen_menu = tk.Menu(menubar, tearoff=0)
        gen_menu.add_command(label="Generate Basic Song", command=self.generate)
        gen_menu.add_command(label="Generate Any Song (Advanced)", command=self.generate_any)
        menubar.add_cascade(label="Generate", menu=gen_menu)
        self.config(menu=menubar)

    def create_toolbar(self):
        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        ttk.Button(toolbar, text="New Song", command=self.generate).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="Play Song", command=self.play_song).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="Save Song", command=self.save_song).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="Show Keyboard", command=self.show_keyboard).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="Oscilloscope", command=self.show_oscilloscope).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="Saved Songs", command=self.show_songs).pack(side=tk.LEFT, padx=2, pady=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

    def create_control_panel(self):
        panel = tk.LabelFrame(self, text="Control Panel", padx=5, pady=5)
        panel.pack(fill=tk.X, padx=10, pady=5)
        # Volume control
        ttk.Label(panel, text="Volume:").pack(side=tk.LEFT)
        self.volume_var = tk.DoubleVar(value=0.2)
        self.volume_slider = ttk.Scale(panel, from_=0, to=1, orient=tk.HORIZONTAL, variable=self.volume_var, length=120)
        self.volume_slider.pack(side=tk.LEFT, padx=5)
        # Tempo control
        ttk.Label(panel, text="Tempo (BPM):").pack(side=tk.LEFT, padx=10)
        self.tempo_var = tk.IntVar(value=120)
        self.tempo_slider = ttk.Scale(panel, from_=60, to=240, orient=tk.HORIZONTAL, variable=self.tempo_var, length=120)
        self.tempo_slider.pack(side=tk.LEFT, padx=5)
        # Play mode
        ttk.Label(panel, text="Play Mode:").pack(side=tk.LEFT, padx=10)
        self.play_mode = ttk.Combobox(panel, values=["Normal", "Loop", "Reverse"])
        self.play_mode.set("Normal")
        self.play_mode.pack(side=tk.LEFT, padx=5)
        # Add Stop button to control panel
        ttk.Button(panel, text="Stop", command=self.stop_playback).pack(side=tk.LEFT, padx=10)
        # Add Mute checkbox to control panel
        self.mute_var = tk.BooleanVar(value=False)
        self.mute_check = ttk.Checkbutton(panel, text="Mute", variable=self.mute_var)
        self.mute_check.pack(side=tk.LEFT, padx=10)

    def stop_playback(self):
        try:
            sd.stop()
        except Exception:
            pass

    def create_widgets(self):
        ttk.Label(self, text="Title:").pack()
        self.title_entry = ttk.Entry(self)
        self.title_entry.pack()
        ttk.Label(self, text="Key:").pack()
        self.key_entry = ttk.Entry(self)
        self.key_entry.insert(0, "C")
        self.key_entry.pack()
        ttk.Label(self, text="Scale:").pack()
        self.scale_entry = ttk.Entry(self)
        self.scale_entry.insert(0, "major")
        self.scale_entry.pack()
        ttk.Label(self, text="Length (bars):").pack()
        self.length_entry = ttk.Entry(self)
        self.length_entry.insert(0, "16")
        self.length_entry.pack()
        ttk.Label(self, text="Clef:").pack()
        self.clef_combo = ttk.Combobox(self, values=["treble", "bass"])
        self.clef_combo.set("treble")
        self.clef_combo.pack()
        ttk.Button(self, text="Generate Song", command=self.generate).pack(pady=10)
        ttk.Button(self, text="Play Song", command=self.play_song).pack(pady=5)
        self.result = tk.Text(self, height=10)
        self.result.pack(fill=tk.BOTH, expand=True)
        self.lyrics_box = tk.Text(self, height=5)
        self.lyrics_box.pack(fill=tk.BOTH, expand=True)
        self.osc_frame = tk.Frame(self)
        self.osc_frame.pack(fill=tk.BOTH, expand=True)
        self.osc_canvas = None
        self.current_song = None
        self.last_wave = None

    def generate(self):
        title = self.title_entry.get()
        key = self.key_entry.get()
        scale = self.scale_entry.get()
        clef = self.clef_combo.get()
        try:
            length = int(self.length_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Length must be an integer.")
            return
        song_data = generate_song(title, key, scale, length, clef, with_lyrics=True)
        self.current_song = song_data
        self.result.delete(1.0, tk.END)
        for n in song_data['notes']:
            self.result.insert(tk.END, f"{n['note']} ({n['duration_name']}, {n['dynamic']}, {n['clef']})\n")
        self.lyrics_box.delete(1.0, tk.END)
        self.lyrics_box.insert(tk.END, song_data['lyrics'])

    def generate_any(self):
        title = self.title_entry.get()
        key = self.key_entry.get()
        scale = self.scale_entry.get()
        clef = self.clef_combo.get()
        try:
            length = int(self.length_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Length must be an integer.")
            return
        song_data = generate_any_song(title, key, scale, length, clef, with_lyrics=True)
        self.current_song = song_data
        self.result.delete(1.0, tk.END)
        for n in song_data['melody']:
            self.result.insert(tk.END, f"{n['note']} ({n['duration']}, {n['clef']})\n")
        self.result.insert(tk.END, "Chords:\n")
        for c in song_data['chords']:
            self.result.insert(tk.END, f"{c['root']}: {c['chord']}\n")
        self.lyrics_box.delete(1.0, tk.END)
        self.lyrics_box.insert(tk.END, song_data['lyrics'])

    def play_song(self):
        if not self.current_song or not self.current_song['notes']:
            messagebox.showinfo("Info", "No song generated.")
            return
        threading.Thread(target=self._play_notes, daemon=True).start()

    def _play_notes(self):
        sample_rate = 44100
        wave = np.array([])
        volume = 0.0 if getattr(self, 'mute_var', None) and self.mute_var.get() else (self.volume_var.get() if hasattr(self, 'volume_var') else 0.2)
        tempo = self.tempo_var.get() if hasattr(self, 'tempo_var') else 120
        play_mode = self.play_mode.get() if hasattr(self, 'play_mode') else "Normal"
        notes = self.current_song['notes'] if 'notes' in self.current_song else self.current_song.get('melody', [])
        if play_mode == "Reverse":
            notes = list(reversed(notes))
        if play_mode == "Loop":
            for _ in range(2):  # Play twice for demo; can be made user-configurable
                for note in notes:
                    freq = note['frequency'] if 'frequency' in note else 440.0
                    duration = note['duration'] * (120 / tempo)
                    t = np.linspace(0, duration, int(sample_rate * duration), False)
                    tone = volume * np.sin(2 * np.pi * freq * t)
                    wave = np.concatenate((wave, tone))
                    sd.play(tone, sample_rate)
                    sd.wait()
            self.last_wave = wave
            return
        for note in notes:
            freq = note['frequency'] if 'frequency' in note else 440.0
            duration = note['duration'] * (120 / tempo)
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            tone = volume * np.sin(2 * np.pi * freq * t)
            wave = np.concatenate((wave, tone))
            sd.play(tone, sample_rate)
            sd.wait()
        self.last_wave = wave

    def show_oscilloscope(self):
        if self.last_wave is None:
            messagebox.showinfo("Info", "No audio to display. Play a song first.")
            return
        if self.osc_canvas:
            self.osc_canvas.get_tk_widget().destroy()
        fig = Figure(figsize=(6, 2), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(self.last_wave[:44100])  # Show first second
        ax.set_title("Oscilloscope View (First Second)")
        ax.set_xlabel("Sample")
        ax.set_ylabel("Amplitude")
        self.osc_canvas = FigureCanvasTkAgg(fig, master=self.osc_frame)
        self.osc_canvas.draw()
        self.osc_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def save_song(self):
        if not self.current_song:
            messagebox.showinfo("Info", "No song to save.")
            return
        title = self.title_entry.get()
        key = self.key_entry.get()
        scale = self.scale_entry.get()
        clef = self.clef_combo.get()
        notes_str = str(self.current_song['notes'])
        lyrics = self.current_song['lyrics']
        save_song(title, key, scale, clef, notes_str, lyrics)
        messagebox.showinfo("Saved", "Song saved to database.")

    def show_songs(self):
        songs = get_songs()
        self.result.delete(1.0, tk.END)
        for s in songs:
            self.result.insert(tk.END, f"{s[1]} ({s[2]} {s[3]} {s[4]})\nLyrics: {s[6]}\n---\n")

    def show_keyboard(self):
        kb_win = tk.Toplevel(self)
        kb_win.title("Virtual Piano Keyboard")
        kb_frame = tk.Frame(kb_win)
        kb_frame.pack()
        white_keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        key_order = []
        for octave in range(1, 8):
            for note in white_keys:
                key_order.append(f"{note}{octave}")
        key_buttons = {}
        for i, note in enumerate(key_order):
            btn = tk.Button(kb_frame, text=note, width=4, height=8, bg='white', command=lambda n=note: self.play_keyboard_note(n))
            btn.grid(row=0, column=i, padx=1, pady=1)
            key_buttons[note] = btn
        # Add black keys
        black_key_offsets = {'C': 0.7, 'D': 1.7, 'F': 3.7, 'G': 4.7, 'A': 5.7}
        for octave in range(1, 8):
            for note, offset in black_key_offsets.items():
                note_name = f"{note}#{octave}"
                col = white_keys.index(note) + (octave - 1) * 7
                btn = tk.Button(kb_frame, text=note_name, width=2, height=4, bg='black', fg='white', command=lambda n=note_name: self.play_keyboard_note(n))
                btn.place(x=(col + offset) * 32, y=0)

    def play_keyboard_note(self, note_name):
        # Find frequency for note_name
        freq = None
        for n in KEYBOARD_NOTES:
            if n['note'] == note_name:
                freq = n['frequency']
                break
        if freq is None:
            return
        sample_rate = 44100
        duration = 0.5
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = 0.2 * np.sin(2 * np.pi * freq * t)
        sd.play(tone, sample_rate)
        sd.wait()

    def create_multitrack_panel(self):
        panel = tk.LabelFrame(self, text="Multi-Track Editor", padx=5, pady=5)
        panel.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        self.track_listbox = tk.Listbox(panel, height=5)
        self.track_listbox.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        self.track_add_btn = ttk.Button(panel, text="Add Track", command=self.add_track)
        self.track_add_btn.pack(side=tk.LEFT, padx=5)
        self.track_remove_btn = ttk.Button(panel, text="Remove Track", command=self.remove_track)
        self.track_remove_btn.pack(side=tk.LEFT, padx=5)
        self.track_name_entry = ttk.Entry(panel)
        self.track_name_entry.pack(side=tk.LEFT, padx=5)
        self.track_instr_combo = ttk.Combobox(panel, values=["Piano", "Guitar", "Drums", "Bass", "Synth"])
        self.track_instr_combo.set("Piano")
        self.track_instr_combo.pack(side=tk.LEFT, padx=5)
        self.tracks = []

    def add_track(self):
        name = self.track_name_entry.get() or f"Track {len(self.tracks)+1}"
        instr = self.track_instr_combo.get()
        track = Track(name, instr)
        self.tracks.append(track)
        self.track_listbox.insert(tk.END, f"{name} ({instr})")

    def remove_track(self):
        sel = self.track_listbox.curselection()
        if sel:
            idx = sel[0]
            self.track_listbox.delete(idx)
            del self.tracks[idx]

if __name__ == "__main__":
    app = MusicGUI()
    app.mainloop()
