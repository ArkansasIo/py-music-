import tkinter as tk
from tkinter import ttk

class MainPage(tk.Frame):
    def __init__(self, master, on_start, on_about, on_help):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets(on_start, on_about, on_help)

    def create_widgets(self, on_start, on_about, on_help):
        title = tk.Label(self, text="Welcome to Music Program", font=("Arial", 24, "bold"))
        title.pack(pady=30)
        subtitle = tk.Label(self, text="Compose, generate, and play music with advanced tools!", font=("Arial", 14))
        subtitle.pack(pady=10)
        start_btn = ttk.Button(self, text="Start Creating Music", command=on_start)
        start_btn.pack(pady=30)
        about_btn = ttk.Button(self, text="About", command=on_about)
        about_btn.pack(pady=5)
        help_btn = ttk.Button(self, text="Help", command=on_help)
        help_btn.pack(pady=5)

class AboutPage(tk.Frame):
    def __init__(self, master, on_back):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        tk.Label(self, text="About Music Program", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(self, text="Version 1.0\nOpen source modular music creation suite.", font=("Arial", 12)).pack(pady=10)
        ttk.Button(self, text="Back", command=on_back).pack(pady=20)

class HelpPage(tk.Frame):
    def __init__(self, master, on_back):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        tk.Label(self, text="Help & Instructions", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(self, text="- Click 'Start Creating Music' to launch the main editor.\n- Use the menu for advanced features.\n- See README.md for more.", font=("Arial", 12)).pack(pady=10)
        ttk.Button(self, text="Back", command=on_back).pack(pady=20)

if __name__ == "__main__":
    class App(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Music Program")
            self.geometry("900x700")
            self.show_main()
        def show_main(self):
            self.clear()
            self.main_page = MainPage(self, self.launch_gui, self.show_about, self.show_help)
        def show_about(self):
            self.clear()
            self.about_page = AboutPage(self, self.show_main)
        def show_help(self):
            self.clear()
            self.help_page = HelpPage(self, self.show_main)
        def launch_gui(self):
            self.clear()
            from ui.music_gui import MusicGUI
            MusicGUI(self)
        def clear(self):
            for widget in self.winfo_children():
                widget.destroy()
    App().mainloop()
