from typing import List, Iterable
from util.note import Note
from util.scale import Scale
from util.scale import MODE_LEN
import numpy as np
import random

class Melody:
    """Class to generate and store sequences of notes (melodies)
    """
    
    __INITIAL_PITCH_MODEL : List[float] = [
        120, 20, 120, 20, 50, 2, 0
    ]
    """The initial random weights for generating the ith pitch in modal space.
    """
    
    notes : List[Note]
    """A list of notes generated for the melody. Pitches are in 
    chromatic space relative to the melody scale root.
    """
    
    length : float
    """Total length of the melody in beats.
    """
    
    __scale : Scale
    """The scale the melody will be placed in.
    """
    
    __model_pitch_range : List[int]
    """The ith element is the pitch in modal space corresponding to
    the ith column in the pitch model. Used to convert from pitch model
    column index to the actual pitch. 
    """
    
    __current_pitch_model : np.array
    """An N x N array where N is the length of the possible melody pitch range. 
    Each column corresponds to the random weight for generating the next note, 
    and each row corresponds to the previous note. 
    """
    
    
    def __init__(self, p_range : tuple[int, int] = (-3, 7)) -> None:
        """Initializes a new melody. Initializes each current random weights row to 
        the initial random weights. 
        
        Args:
            p_range: A tuple defining a range [a,b) of possible pitches in modal space. 
        """
        # When initializing, extend the initial model to the extent of p_range. 
        self.__model_pitch_range = range(p_range[0], p_range[1])
        extended_initial : List[float] = [
            self.__INITIAL_PITCH_MODEL[pitch % MODE_LEN] for pitch in self.__model_pitch_range
        ]
        self.__current_pitch_model = np.array([
            extended_initial for _ in self.__model_pitch_range
        ])
        
    
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
        
        # Generate pitches and durations as column indices
        generated : List[int] = []
        prev_pitch : int = 0
        pos : float = 0.0
        
        while pos < self.length:
            generated_duration = .5
            generated.append((
                self.__generate_pitch(prev_pitch),
                generated_duration
            ))
            # TODO - update model weights
            # TODO - generate note durations using a similar model, but some notes will need to be aligned/filled on the beat
            pos += generated_duration
        
        # Populate notes from the given pitches and durations
        pos : float = 0.0
        self.notes = []
        
        for col, duration in generated:
            # using the min() function to trim to desired length. 
            self.notes.append(scale[self.__model_pitch_range[col]].init(min(
                duration, self.length - pos
            ), pos))
            pos += duration
    
    
    def __generate_pitch(self, prev_pitch : int) -> int:
        """Randomly generates a pitch as column index in the model according to
        the previous pitch.  

        Args:
            prev_pitch: The previous pitch as a column index in the model. 
            
        Returns:
            The generated pitch as a column index. 
        """
        weights : List[float] = self.__current_pitch_model[prev_pitch]
        return random.choices(population=range(len(weights)), weights=weights, k=1)[0]