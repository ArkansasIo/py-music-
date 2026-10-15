from pymusic.theory import *

def test_frequency_round_trip():
    assert abs(note_to_freq("A",4)-440.0) < 1e-9
    assert freq_to_note(440.0)==("A",4)

def test_scales_and_chords():
    assert get_scale("C","major")[:-1]==["C","D","E","F","G","A","B"]
    assert get_chord("C","maj7")==["C","E","G","B"]

def test_transpose():
    assert transpose("C",7)=="G"
