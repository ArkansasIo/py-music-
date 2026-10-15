from pymusic.models import Song, Track, NoteEvent

def test_song_round_trip():
    s=Song("Test"); t=Track("Piano"); t.add(NoteEvent(60,0,1)); s.add_track(t)
    assert Song.from_dict(s.to_dict()).to_dict()==s.to_dict()
