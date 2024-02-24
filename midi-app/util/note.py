from typing_extensions import Self

class Note:
    """Structure to store a note's relative pitch, duration, and position.
    """
    
    pitch : int
    """The pitch of the note, relative to a chromatic scale. 
    """
    
    duration : float
    """The duration of the note in beats. 
    """
    
    position : float
    """The relative time the note should start in beats.
    """
    
    def __init__(self, pitch : int = 0, duration : float = 0.0, position : float = 0.0) -> None:
        """Initialize a note.
        
        Args:
            pitch: The pitch of the note, relative to a chromatic scale. 
            duration: The duration of the note in beats. 
            position: The relative time the note should start in beats.
        """
        self.pitch = pitch
        self.duration = duration
        self.position = position
        
        
    def init(self, duration : float = 0.0, position : float = 0.0) -> Self:
        """Function to finish initializing a note with only a pitch. 

        Args:
            duration: The duration of the note in beats. 
            position: The relative time the note should start in beats.
            
        Returns:
            self
        """
        self.duration = duration
        self.position = position
        return self
        
        
    def __repr__(self) -> str:
        """Function for printing representation. 

        Returns:
            str: the string representation of a note object. 
        """
        return f'Note data: pitch={self.pitch} duration={self.duration} position={self.position}'
    