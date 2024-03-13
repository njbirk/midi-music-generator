from util.melody import Melody
from util.scale import Mode, Scale
from out import OutputHandler

def generate_midi(filename : str = "out"):
    
    # Create simple melody for testing purposes. 
    melody : Melody = Melody()
    melody.generate(
        scale=Scale(Mode.Aeolian),
        length=4,
        epsilon=.5,
        alignment=1
    )
    
    # Generate MIDI file and output MP3
    handler = OutputHandler()
    handler.add_melody(melody)
    handler.write(filename)


if __name__ == '__main__':
    generate_midi()
