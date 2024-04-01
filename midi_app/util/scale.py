from enum import Enum
from .note import Note
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


class ModeOffsets_map(TypedDict):
    """A class to correctly type the mode offsets dictionary. 
    """
    quotient : int
    offset : int
    
    
MODE_OFFSETS : ModeOffsets_map = {
    3 : 3,
    2 : 0,
    1 : 4,
    0 : 1,
    -1 : 5,
    -2 : 2,
    -3 : 6
}
"""A dictionary that maps a DBQ to its offset relative to Ionian. 
"""


class DBQName_map(TypedDict):
    """A class to correctly type the dbq name dictionary. 
    """
    quotient : int
    name : List[str]
    
    
DBQ_NAMES : DBQName_map = {
    3 : ['IV', 'VI'],
    2 : ['I', 'III'],
    1 : ['V', 'VII'],
    0 : ['ii', 'iv'],
    -1 : ['vi', 'i'],
    -2 : ['iii', 'v'],
    -3 : ['viio', 'iio']
}
"""A dictionary that maps a DBQ to its [major name, minor name].
"""
    

class ModePitches_map(TypedDict):
    """A class to correctly type the mode pitches dictionary. 
    """
    mode : Mode
    offsets : List[int]
    

MODE_PITCHES : ModePitches_map = {
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


class DBQ_map(TypedDict):
    """A class to correctly type the mode pitches dictionary. 
    """
    mode : Mode
    quotient : int
    

MODE_DBQ : DBQ_map = {
    Mode.Lydian : 3,
    Mode.Ionian : 2,
    Mode.Mixolydian : 1,
    Mode.Dorian : 0,
    Mode.Aeolian : -1,
    Mode.Phrygian : -2,
    Mode.Locrian : -3
}
"""A dictionary that maps a mode to its dorian brightness
quotient. >0 is 'major' sounding and <=0 is 'minor' sounding. 
Adjaent quotients also signify adjacency on the circle of fifths. 
"""


def dbq_to_mode_complex(dbq : int) -> Mode:
    """Converts a dorian brightness quotient to a mode. 
    """
    for mode in MODES:
        if MODE_DBQ[mode] == dbq:
            return mode
    assert False, f'Invalid DBQ: {dbq}'


def dbq_to_mode_simple(dbq : int) -> Mode:
    """Converts a dorian brightness quotient to a mode. 
    """
    return Mode.Ionian if dbq > 0 else Mode.Aeolian


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
        in modal space to a pitch in chromatic space. This is extended
        for any integer i. The note pitches are relative to the first 
        note in the scale. Durations and positions are uninitialized. 
        """
        return MODE_PITCHES[self.__mode][mode_pitch % MODE_LEN] + (mode_pitch // MODE_LEN) * CHROMA_LEN
    
    
    def __repr__(self) -> str:
        """Function for printing representation. 

        Returns:
            str: the string representation of a scale object. 
        """
        return f'Scale data: mode={self.__mode}'
    
