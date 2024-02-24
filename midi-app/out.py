from midiutil import MIDIFile
from util.melody import Melody
from util.note import Note

class OutputHandler:
    """Class to wrap all the MIDI output code. 
    """
    
    __file : MIDIFile
    """The output file object.
    """
    
    __NC : float
    """The note counter. Keeps track of where in the output
    song we are writting in beats. 
    """
    
    
    __key : int
    """The starting song pitch. 
    """
    
    def __init__(self, tempo : int = 110, key : int = 50) -> None:
        """Initialize the output handler.
        
        Args:
            tempo: Tempo in BPM.
            key: Key in absolute note position. 
        """
        
        self.__NC = 0
        self.__key = key
        
        self.__file = MIDIFile(1)
        self.__file.addTrackName(0, 0, 'Melody')
        self.__file.addProgramChange(0, 0, 0, 0)
        self.__file.addTempo(0, 0, tempo)
        
            
    def write(self) -> None:
        """Function to perform the final step of writing to a MIDI file.
        """
        with open('out/out.mid', 'wb') as output_file:
            self.__file.writeFile(output_file)
            
    
    def add_melody(self, melody : Melody) -> None:
        """Temporary function that write a simple melody to the file
        in the root position of the key.

        Args:
            melody: The melody to add. 
        """
        
        for note in melody.notes:
            
            global_pitch = self.__key + note.pitch
            
            # Validate pitch and duration
            assert 0 <= global_pitch <= 127, f'{global_pitch} is not a valid note pitch'
            assert note.duration > 0, f'{note.duration} is not a valid note duration'

            self.__file.addNote(
                track=0,
                channel=0,
                volume=75,
                pitch=global_pitch,
                time=self.__NC + note.position,
                duration=note.duration
            )
        self.__NC += melody.length