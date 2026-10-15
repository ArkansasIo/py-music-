from pymusic.composer import SongGenerator

def test_deterministic_generation():
    a=SongGenerator(7).song("A","C","major",4).to_dict()
    b=SongGenerator(7).song("A","C","major",4).to_dict()
    assert a==b

def test_duration_positive():
    song=SongGenerator(1).song(bars=2)
    assert song.duration>0
    assert all(n.duration>0 for t in song.tracks for n in t.notes)
