from midiutil import MIDIFile
from util.melody import Melody
from util.note import Note
from util.note import INSTRUMENTS
from midi2audio import FluidSynth

class OutputHandler:
    """Class to wrap all the MIDI output code. 
    """


    __CHANNEL : int = 0
    """The MIDI channel to output to
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
        
        self.__file = MIDIFile(numTracks=1)
        self.__file.addTrackName(0, 0, 'Melody')
        self.__file.addProgramChange(0, self.__CHANNEL, 0, INSTRUMENTS['Acoustic Grand Piano'])
        self.__file.addTempo(0, 0, tempo)
        
            
    def write(self, filename : str) -> None:
        """Function to perform the final step of writing to a MIDI file.
        Also converts to MP3. 
        """
        midi_path = 'out/out.mid'
        mp3_path = 'out/' + filename + '.wav'
        with open(midi_path, 'wb') as output_file:
            self.__file.writeFile(output_file)

        # Convert MIDI to WAV
        FluidSynth(sound_font='font.sf2').midi_to_audio(midi_path, mp3_path)
            
    
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
                channel=self.__CHANNEL,
                volume=75,
                pitch=global_pitch,
                time=self.__NC + note.position,
                duration=note.duration
            )
        self.__NC += melody.length