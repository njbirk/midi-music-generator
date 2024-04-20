from .util.melody import Melody
from .util.scale import Mode, Scale
from .util.progression import Progression
from .out import OutputHandler
import numpy as np

speed_map = {
    "slow": 80,
    "medium": 110,
    "fast": 140
}

tone_map = {
    "happy": Mode.Ionian,
    "sad": Mode.Aeolian,
}

volume_map = {
    "quiet": 50,
    "medium": 75,
    "loud": 100
}

instrument_map = {
    "piano": "Acoustic Grand Piano",
    "electric piano": "Electric Grand Piano",
}

def repeatability_map(repeatability : str) -> float:
    b = 1.6
    return 50 * b ** (int(repeatability) - 10)

def structuredness_map(structuredness : str) -> int:
    b = 0.34
    return np.floor(b * int(structuredness))

def generate_midi(filename : str = "out", params : list = [
    "medium", "happy", "medium", "piano", "5", "5"
]):

    # Parse args
    (speed, tone, volume, instrument, repeatability, structuredness) \
    = (params[0], params[1], params[2], params[3], params[4], params[5])

    
    # Create base melody and a test chord progression
    melody : Melody = Melody(
        p_range=(-2, 6),
        d_range=(-2, 3)
    )
    melody.generate(
        length=2,
        epsilon=repeatability_map(repeatability),
        alignment=structuredness_map(structuredness)
    )
    
    progression : Progression = Progression()
    progression.generate_from_one(
        melody=melody,
        tone=tone_map[tone],
        length_range=(2, 4) 
    )
    print(progression)
    
    # Generate MIDI file and output MP3
    handler = OutputHandler(tempo=speed_map[speed], key=50, 
        instrument=instrument_map[instrument], volume=volume_map[volume])
    for _ in range(2):
        handler.write_notes(progression.notes)
    handler.write(filename)


if __name__ == '__main__':
    generate_midi()
