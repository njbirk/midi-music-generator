from .util.melody import Melody
from .util.scale import Mode, Scale
from .util.progression import Progression
from .out import OutputHandler

def generate_midi(filename : str = "out"):
    
    # Create base melody and a test chord progression
    melody : Melody = Melody(
        p_range=(-2, 6),
        d_range=(-2, 3)
    )
    melody.generate(
        length=2,
        epsilon=.5,
        alignment=1
    )
    
    progression : Progression = Progression()
    progression.generate_from_one(
        melody=melody,
        tone=Mode.Aeolian,
        length_range=(2, 4) 
    )
    print(progression)
    
    # Generate MIDI file and output MP3
    handler = OutputHandler(tempo=110, key=50, instrument='Acoustic Grand Piano')
    for _ in range(2):
        handler.write_notes(progression.notes)
    handler.write(filename)


if __name__ == '__main__':
    generate_midi()
