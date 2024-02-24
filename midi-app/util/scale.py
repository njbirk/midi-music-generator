from enum import Enum
from util.note import Note
from typing import List, TypedDict


class Mode(Enum):
    """An enum to specify the 7 different modes. 
    """
    Lydian = 1
    Ionian = 2
    Mixolydian = 3
    Dorian = 4
    Aeolian = 5
    Phrygian = 6
    Locrian = 7
    
    
MODES : List[Mode] = [
    Mode.Ionian,
    Mode.Dorian,
    Mode.Phrygian,
    Mode.Lydian,
    Mode.Mixolydian,
    Mode.Aeolian,
    Mode.Locrian
]
"""A list of modes, where the ith mode corresponds to the mode 
starting at position i in modal space. 
"""
    

class ModePitches(TypedDict):
    """A class to correctly type the mode pitches dictionary. 
    """
    mode : Mode
    offsets : List[int]
    

MODE_PITCHES : ModePitches = {
    Mode.Lydian : [0, 2, 4, 6, 7, 9, 11, 12],
    Mode.Ionian : [0, 2, 4, 5, 7, 9, 11, 12],
    Mode.Mixolydian : [0, 2, 4, 5, 7, 9, 10, 12],
    Mode.Dorian : [0, 2, 3, 5, 7, 9, 10, 12],
    Mode.Aeolian : [0, 2, 3, 5, 7, 8, 10, 12],
    Mode.Phrygian : [0, 1, 3, 5, 7, 8, 10, 12],
    Mode.Locrian : [0, 1, 3, 5, 6, 8, 10, 12]
}
"""A dictionary that maps a mode to its pitch offsets. 
Accessing the ith offset will convert pitch i
in modal space to a pitch in chromatic space. 
"""


MODE_LEN : int = 7
"""The note offset defining an octave for a modal scale.
"""

CHROMA_LEN : int = 12
"""The note offset defining an octave for a chromatic scale. 
"""


class Scale:
    """Class to store information on a scale.
    """
    
    __mode : Mode
    
    def __init__(self, mode : Mode) -> None:
        """Creates a new scale object from a mode."""
        self.__mode = mode
            
    
    def __getitem__(self, mode_pitch : int) -> Note:
        """Accessing the ith note will convert pitch i
        in modal space to a note in chromatic space. This is extended
        for any integer i. The note pitches are relative to the first 
        note in the scale. Durations and positions are uninitialized. 
        """
        octave : int = mode_pitch // MODE_LEN
        chroma_pitch : int = MODE_PITCHES[self.__mode][mode_pitch % MODE_LEN] + octave * CHROMA_LEN
        return Note(pitch=chroma_pitch)
    
    
    def __repr__(self) -> str:
        """Function for printing representation. 

        Returns:
            str: the string representation of a scale object. 
        """
        return f'Scale data: mode={self.__mode}'
    
