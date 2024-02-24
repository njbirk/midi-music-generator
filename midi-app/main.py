from util.melody import Melody
from util.scale import Mode, Scale
from out import OutputHandler

def generate_midi():
    
    # Create simple melody for testing purposes. 
    melody : Melody = Melody()
    melody.generate(Scale(Mode.Ionian))
    
    # Generate MIDI file
    handler = OutputHandler()
    handler.add_melody(melody)
    handler.write()


if __name__ == '__main__':
    generate_midi()
