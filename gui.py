import tkinter as tk
from tkinter import ttk, messagebox
from music import generate_song
from db import init_db, save_song, get_songs
import threading
import sounddevice as sd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class MusicGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Program")
        self.geometry("700x700")
        init_db()
        self.create_widgets()

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
        ttk.Button(self, text="Show Oscilloscope", command=self.show_oscilloscope).pack(pady=5)
        ttk.Button(self, text="Save Song", command=self.save_song).pack(pady=5)
        ttk.Button(self, text="Show Saved Songs", command=self.show_songs).pack(pady=5)

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

    def play_song(self):
        if not self.current_song or not self.current_song['notes']:
            messagebox.showinfo("Info", "No song generated.")
            return
        threading.Thread(target=self._play_notes, daemon=True).start()

    def _play_notes(self):
        sample_rate = 44100
        wave = np.array([])
        for note in self.current_song['notes']:
            freq = note['frequency']
            duration = note['duration']
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            tone = 0.2 * np.sin(2 * np.pi * freq * t)
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

if __name__ == "__main__":
    app = MusicGUI()
    app.mainloop()
