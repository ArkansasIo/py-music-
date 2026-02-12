from fastapi import FastAPI
from music import generate_song

app = FastAPI()

@app.get("/generate")
def generate(title: str = "Untitled", key: str = "C", scale: str = "major", length: int = 16, clef: str = "treble"):
    """Generate a song using music theory parameters."""
    song = generate_song(title=title, key=key, scale=scale, length=length, clef=clef)
    return {"title": title, "key": key, "scale": scale, "length": length, "clef": clef, "notes": song}
