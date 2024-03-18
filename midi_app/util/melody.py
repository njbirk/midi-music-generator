from typing import List, Iterable, Optional
from .note import Note
from .scale import Scale
from .scale import MODE_LEN
import numpy as np
import random

class Melody:
    """Class to generate and store sequences of notes (melodies)
    """
    
    __INITIAL_PITCH_MODEL : List[float] = [
        8., 2., 8., 2., 5., 2., 0.
    ]
    """The initial random weights for generating the ith pitch in modal space.
    """
    
    def __INITIAL_DURATION_MODEL(self, duration : float) -> float:
        """A distribution that defines the initial duration model. Currently
        uses a bell curve with respect to the logarithm of duration. To modify, 
        would recommend using Desmos for visualization. 

        Args:
            duration: The input duration in beats.

        Returns:
            The weight corresponding to that duration. 
        """
        width : float = .7
        offset : float = -1
        return np.exp(-1 * (width * (np.log(duration) - offset))**2)
    
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
    
    __model_duration_range : List[float]
    """The ith element is the duration corresponding to
    the ith column in the duration model. Used to convert from duration model
    column index to the actual duration. 
    """
    
    __current_pitch_model : np.array
    """An N x N array where N is the length of the possible melody pitch range. 
    Each column corresponds to the random weight for generating the next note, 
    and each row corresponds to the previous note. 
    """
    
    __current_duration_model : np.array
    """An N x N array where N is the length of the possible melody duration range. 
    Each column corresponds to the random weight for generating the next duration, 
    and each row corresponds to the previous duration. 
    """
    
    __epsilon : float
    __epsilon_pitch : float
    __epsilon_duration : float
    """Model parameters that determine the strength of weight updates. 
    """
    
    
    def __init__(self, p_range : 'tuple[int, int]' = (-3, 7), d_range : 'tuple[int, int]' = (-2, 1)) -> None:
        """Initializes a new melody. Initializes each current random weights row to 
        the initial random weights. 
        
        Args:
            p_range: A tuple defining a range [a,b) of possible pitches in modal space. 
            d_range: A tuple defining a logarithmic range [a,b) -> [2^a, 2^b) of possible durations. 
        """
        # When initializing, extend the initial model to the extent of p_range. 
        self.__model_pitch_range = range(p_range[0], p_range[1])
        self.__model_duration_range = [2**i for i in range(d_range[0], d_range[1])]
        
        self.__current_pitch_model = np.array([
            [self.__INITIAL_PITCH_MODEL[pitch % MODE_LEN] for pitch in self.__model_pitch_range]
            for _ in self.__model_pitch_range
        ])
        self.__current_duration_model = np.array([
            [self.__INITIAL_DURATION_MODEL(duration) for duration in self.__model_duration_range]
            for _ in self.__model_duration_range
        ])
        
    
    def __repr__(self) -> str:
        """Function for printing representation. 

        Returns:
            str: the string representation of a melody. 
        """
        out : str = f'Melody data:\n{self.__scale.__repr__()}\n'
        for note in self.notes:
            out += f'{note.__repr__()}\n'
        return out
    
    
    def generate(self, scale : Scale, length : int = 4, epsilon : float = 10, alignment : Optional[int] = 1) -> None:
        """Generates the melody from scratch, populating the notes list.
        
        Args:
            scale: The scale to generate the melody in.
            length: The total length of the melody in beats. 
            epsilon: Parameter that determines how likely the melody repeats itself. 
            alignment: If defined, determines the minimum splitting of length to align notes to. Higher values
                will result in more syncopated melodies. The min split value will be 2 ^ -alignment. 
        """
        self.__scale = scale
        self.length = length
        self.__epsilon = epsilon
        self.__init_epsilon()
        
        # Generate pitches and durations as column indices
        generated : List[int] = []
        prev_pitch : int = 0
        prev_duration : float = 0
        pos : float = 0.0
        
        while pos < self.length:
            generated_pitch = self.__generate_pitch(prev_pitch)
            generated_duration = self.__generate_duration(prev_duration, pos, alignment)
            generated.append((generated_pitch, generated_duration))
            self.__update_model_weights(
                prev_pitch=prev_pitch,
                prev_duration=prev_duration,
                target_pitch=generated_pitch,
                target_duration=generated_duration
            )
            
            pos += self.__model_duration_range[generated_duration]
            prev_pitch = generated_pitch
            prev_duration = generated_duration
        
        # Populate notes from the given pitches and durations
        # Performance improvement (if needed) - combine this into the above while loop. 
        pos : float = 0.0
        self.notes = []
        
        for col, duration_index in generated:
            duration = self.__model_duration_range[duration_index]
            # using the min() function to trim to desired length. 
            if self.length - pos > 0:
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
    
    
    def __generate_duration(self, prev_duration : int, pos : int, alignment : Optional[int]) -> int:
        """Randomly generates a duration as column index in the model according to
        the previous duration.  

        Args:
            prev_duration: The previous pitch as a column index in the model. 
            pos: The current position in the melody. Used to keep track of alignment. 
            alignment: If defined, determines the minimum splitting of length to align notes to. Higher values
                will result in more syncopated melodies. The min split duration will be 2 ^ -alignment * length. 
            
        Returns:
            The generated duration as a column index. 
        """
        weights : List[float] = self.__current_duration_model[prev_duration]
        population : List[int] = range(len(weights))
        
        if alignment != None:
            L : float = 2 ** (-1 * alignment) * self.length
            max_duration = L * (pos // L + 1) - pos
            population = [i for i in population if self.__model_duration_range[i] <= max_duration]
            weights = [weights[i] for i in population]
        
        return random.choices(population=population, weights=weights, k=1)[0]
    
    
    def __update_model_weights(self, prev_pitch : int, prev_duration : int, target_pitch : int, target_duration : int) -> None:
        """Updates the pitch and duration models based on which target note was just generated. 

        Args:
            target_pitch: The target pitch as a column index in the model. 
            target_duration: The target duration as a column index in the model. 
        """
        self.__current_pitch_model[prev_pitch][target_pitch] += self.__epsilon_pitch
        self.__current_duration_model[prev_duration][target_duration] += self.__epsilon_duration
        
    
    def __init_epsilon(self):
        """Initializes the pitch and duration epsilons based on epsilon. 
        """
        self.__epsilon_pitch = np.sum(self.__current_pitch_model[0]) * self.__epsilon / len(self.__current_pitch_model[0])
        self.__epsilon_duration = np.sum(self.__current_duration_model[0]) * self.__epsilon / len(self.__current_duration_model[0])
        
        
