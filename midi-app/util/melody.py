from typing import List, Iterable
from util.note import Note
from util.scale import Scale
import numpy as np

class Melody:
    """Class to generate and store sequences of notes (melodies)
    """
    
    notes : List[Note]
    """A list of notes generated for the melody. Pitches are in 
    chromatic space relative to the melody scale root.
    """
    
    __scale : Scale
    
    length : float
    """Total length of the melody in beats.
    """
    
    def __init__(self) -> None:
        """Initializes a new melody.
        """
        pass
    
    
    def __repr__(self) -> str:
        """Function for printing representation. 

        Returns:
            str: the string representation of a melody. 
        """
        out : str = f'Melody data:\n{self.__scale.__repr__()}\n'
        for note in self.__notes:
            out += f'{note.__repr__()}\n'
        return out
    
    
    def generate(self, scale : Scale, length : int = 4) -> None:
        """Generates the melody from scratch, populating the notes list.
        
        Args:
            scale: The scale to generate the melody in.
            length: The total length of the melody in beats. 
        """
        self.__scale = scale
        self.length = length
        
        # TODO : Implement actual generation, this is just a test melody
        self.notes = [scale[0].init(1, 0), scale[-2].init(1, 1)]
        
    
    
    def generate_variation(self, scale : Scale, variability : float) -> None:
        """Generates the melody similar to an existing one, populating the notes list.
        
        Args:
            scale: The scale to generate the melody in.
        """
        
        # TODO : Implement this
        pass