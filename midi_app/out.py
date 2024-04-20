import os
from midiutil import MIDIFile
from .util.melody import Melody
from .util.progression import Progression
from .util.note import Note
from .util.note import INSTRUMENTS
from midi2audio import FluidSynth
from typing import List

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

    __volume : int
    """The volume of each note.
    """
    
    def __init__(self, tempo : int = 110, key : int = 50, instrument : str = 'Harpsichord',
                 volume : int = 100) -> None:
        """Initialize the output handler.
        
        Args:
            tempo: Tempo in BPM.
            key: Key in absolute note position. 
        """
        
        self.__NC = 0
        self.__key = key
        self.__volume = volume
        
        self.__file = MIDIFile(numTracks=1)
        self.__file.addTrackName(0, 0, 'Melody')
        self.__file.addProgramChange(0, self.__CHANNEL, 0, INSTRUMENTS[instrument])
        self.__file.addTempo(0, 0, tempo)
        
            
    def write(self, filename : str) -> None:
        """Function to perform the final step of writing to a MIDI file.
        Also converts to MP3. 
        """
        out_dir = 'out'
        midi_path = os.path.join(out_dir, 'out.mid')
        mp3_path = os.path.join(out_dir, filename + '.wav')
        
        # Ensure the output directory exists
        os.makedirs(out_dir, exist_ok=True)
        with open(midi_path, 'wb') as output_file:
            self.__file.writeFile(output_file)

        # Convert MIDI to WAV
        FluidSynth(sound_font='font.sf2').midi_to_audio(midi_path, mp3_path)
            
    
    def write_notes(self, notes : List[Note]) -> None:
        """Function that writes a list of notes to MIDI data
        in the root position of the key.

        Args:
            notes: The notes to add. 
        """
        total_duration : float = 0
        for note in notes:
            
            global_pitch = self.__key + note.pitch
            
            # Validate pitch and duration
            assert 0 <= global_pitch <= 127, f'{global_pitch} is not a valid note pitch'
            assert note.duration > 0, f'{note.duration} is not a valid note duration'

            total_duration += note.duration
            self.__file.addNote(
                track=0,
                channel=self.__CHANNEL,
                volume=self.__volume,
                pitch=global_pitch,
                time=self.__NC + note.position,
                duration=note.duration
            )
        self.__NC += total_duration
