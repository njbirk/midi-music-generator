from typing import List, Iterable, Optional, Literal
from .scale import Mode, dbq_to_mode_complex, dbq_to_mode_simple, MODE_OFFSETS, Scale, DBQ_NAMES
from .note import Note
from .melody import Melody
import numpy as np
import random

class Progression:
    """Class to generate and store chord progressions. 
    """
    
    
    __DBQs : List[int] = [3, 2, 1, 0, -1, -2, -3]
    """The ith element is the dorian brightness quotient corresponding to
    the ith column in the model. Used to convert from model column index to the actual DBQ.
    """

    
    def __INITIAL_MODEL(self, DBQ : int, offset : int) -> float:
        """A distribution that defines the initial model. Currently
        uses a bell curve. To modify, would recommend using Desmos for visualization. 

        Args:
            DBQ: The input dorian brightness quotient.
            offset: The center of the distribution

        Returns:
            The weight corresponding to that DBQ. 
        """
        if DBQ == offset:
            return 0  # Don't want to generate the same chord.
        
        width : float = .4
        return np.exp(-1 * (width * (DBQ - offset))**2)
    
    
    __current_model : np.array
    """An 7 x 7 array. Each column corresponds to the random weight for 
    generating the next DBQ, and each row corresponds to the previous DBQ.
    """
    
    
    __tone : Mode
    """The mode of the root chord. 
    """
    
    
    __progression_data : List[int]
    """A list of dbqs that make up the progression."""
    
    
    notes : List[Note]
    """A list of notes generated as a sequence of melodes. Pitches are in 
    chromatic space relative to the tonic.
    """
    
    
    def __init__(self) -> None:
        """Initializes a new chord progression. 
        
        Args:
            None
        """
        self.notes = []
        self.__current_model = np.array([
            [self.__INITIAL_MODEL(dbq, previous) for dbq in self.__DBQs]
            for previous in self.__DBQs
        ])
        
        
    def __build_progression(self, tone : Mode, length_range : 'tuple[int, int]') -> None:
        """Generates the DBQ values in the progression from scratch.
        
        Args:
            tone: Whether the progression is major (Ionian) or minor (Aeolian).
            length: The desired range of total chords in the progression. If the tonic is reached in
                    this range, the progression will end.
        """
        generated : List[int] = []
        pos : int = 0
        root_dbq : int = 1 if tone == Mode.Ionian else 4
        prev_dbq : int = root_dbq
        
        while True:
            # Limit the length of the progression
            if pos >= length_range[0] and prev_dbq == root_dbq:
                break
            if pos >= length_range[1]:
                break
                
            # Generate the next chord (as column index in the model)
            generated.append(prev_dbq)
            prev_dbq = self.__generate_dbq(prev_dbq)
            pos += 1
            
        self.__progression_data = [self.__DBQs[col] for col in generated]
    
    
    def generate_from_one(self, melody : Melody, tone : Mode = Mode.Aeolian, 
                          length_range : 'tuple[int, int]' = (3, 5)) -> None:
        """Generates the progression on top of a melody.
        
        Args:
            melody: The melody included in each chord. This should be pre-generated. 
            tone: Whether the progression is major (Ionian) or minor (Aeolian).
            length: The desired range of total chords in the progression. If the tonic is reached in
                    this range, the progression will end.
        """
        self.__tone = tone
        
        # Validate params
        assert tone in [Mode.Aeolian, Mode.Ionian], f'{tone} is not Aeolian or Ionian.'
        assert length_range[0] > 0, f'{length_range[0]} is not a valid minimum length.'
        assert length_range[1] >= length_range[0], f'{length_range[1]} is not greater than {length_range[0]}.'

        # Generate the melodies from the built progression
        last_pos : float = 0.0
        self.__build_progression(tone, length_range)
        for dbq in self.__progression_data:
            
            # Generate melodies, get the pitch offsets from the DBQ using an ionian scale
            ionian : Scale = Scale(Mode.Ionian)
            melody.populate_notes(
                scale=Scale(dbq_to_mode_complex(dbq)), 
                pitch_offset=ionian[MODE_OFFSETS[dbq]],
                pos_offset=last_pos
            )
            last_pos += melody.length
            
            # Extract melody notes, append to the list of notes
            self.notes += melody.notes
            
        
    def __generate_dbq(self, prev_dbq : int) -> int:
        """Randomly generates a dbq as column index in the model according to
        the previous duration.

        Args:
            prev_dbq: The previous dbq as a column index.   
        Returns:
            The generated dbq as a column index. 
        """
        
        weights : List[float] = self.__current_model[prev_dbq]
        return random.choices(population=range(len(weights)), weights=weights, k=1)[0]
            
            
    
    def __repr__(self) -> str:
        """Function for printing representation. 

        Returns:
            str: the string representation of a progression. 
        """
        out : str = f'Progression data:'
        for dbq in self.__progression_data:
            out += f' {DBQ_NAMES[dbq][0 if self.__tone == Mode.Ionian else 1]}'
        return out + '\n'
        
