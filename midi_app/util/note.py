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
        
        
    def __repr__(self) -> str:
        """Function for printing representation. 

        Returns:
            str: the string representation of a note object. 
        """
        return f'Note data: pitch={self.pitch} duration={self.duration} position={self.position}'
    

INSTRUMENTS = {
    'Acoustic Grand Piano': 0,
    'Bright Acoustic Piano': 1,
    'Electric Grand Piano': 2,
    'Honky-tonk Piano': 3,
    'Electric Piano 1': 4,
    'Electric Piano 2': 5,
    'Harpsichord': 6,
    'Clavi': 7,
    'Celesta': 8,
    'Glockenspiel': 9,
    'Music Box': 10,
    'Vibraphone': 11,
    'Marimba': 12,
    'Xylophone': 13,
    'Tubular Bells': 14,
    'Dulcimer': 15,
    'Drawbar Organ': 16,
    'Percussive Organ': 17,
    'Rock Organ': 18,
    'Church Organ': 19,
    'Reed Organ': 20,
    'Accordion': 21,
    'Harmonica': 22,
    'Tango Accordion': 23,
    'Acoustic Guitar (nylon)': 24,
    'Acoustic Guitar (steel)': 25,
    'Electric Guitar (jazz)': 26,
    'Electric Guitar (clean)': 27,
    'Electric Guitar (muted)': 28,
    'Overdriven Guitar': 29,
    'Distortion Guitar': 30,
    'Guitar harmonics': 31,
    'Acoustic Bass': 32,
    'Electric Bass (finger)': 33,
    'Electric Bass (pick)': 34,
    'Fretless Bass': 35,
    'Slap Bass 1': 36,
    'Slap Bass 2': 37,
    'Synth Bass 1': 38,
    'Synth Bass 2': 39,
    'Violin': 40,
    'Viola': 41,
    'Cello': 42,
    'Contrabass': 43,
    'Tremolo Strings': 44,
    'Pizzicato Strings': 45,
    'Orchestral Harp': 46,
    'Timpani': 47,
    'String Ensemble 1': 48,
    'String Ensemble 2': 49,
    'SynthStrings 1': 50,
    'SynthStrings 2': 51,
    'Choir Aahs': 52,
    'Voice Oohs': 53,
    'Synth Voice': 54,
    'Orchestra Hit': 55,
    'Trumpet': 56,
    'Trombone': 57,
    'Tuba': 58,
    'Muted Trumpet': 59,
    'French Horn': 60,
    'Brass Section': 61,
    'SynthBrass 1': 62,
    'SynthBrass 2': 63,
    'Soprano Sax': 64,
    'Alto Sax': 65,
    'Tenor Sax': 66,
    'Baritone Sax': 67,
    'Oboe': 68,
    'English Horn': 69,
    'Bassoon': 70,
    'Clarinet': 71,
    'Piccolo': 72,
    'Flute': 73,
    'Recorder': 74,
    'Pan Flute': 75,
    'Blown Bottle': 76,
    'Shakuhachi': 77,
    'Whistle': 78,
    'Ocarina': 79,
    'Lead 1 (square)': 80,
    'Lead 2 (sawtooth)': 81,
    'Lead 3 (calliope)': 82,
    'Lead 4 (chiff)': 83,
    'Lead 5 (charang)': 84,
    'Lead 6 (voice)': 85,
    'Lead 7 (fifths)': 86,
    'Lead 8 (bass + lead)': 87,
    'Pad 1 (new age)': 88,
    'Pad 2 (warm)': 89,
    'Pad 3 (polysynth)': 90,
    'Pad 4 (choir)': 91,
    'Pad 5 (bowed)': 92,
    'Pad 6 (metallic)': 93,
    'Pad 7 (halo)': 94,
    'Pad 8 (sweep)': 95,
    'FX 1 (rain)': 96,
    'FX 2 (soundtrack)': 97,
    'FX 3 (crystal)': 98,
    'FX 4 (atmosphere)': 99,
    'FX 5 (brightness)': 100,
    'FX 6 (goblins)': 101,
    'FX 7 (echoes)': 102,
    'FX 8 (sci-fi)': 103,
    'Sitar': 104,
    'Banjo': 105,
    'Shamisen': 106,
    'Koto': 107,
    'Kalimba': 108,
    'Bag pipe': 109,
    'Fiddle': 110,
    'Shanai': 111,
    'Tinkle Bell': 112,
    'Agogo': 113,
    'Steel Drums': 114,
    'Woodblock': 115,
    'Taiko Drum': 116,
    'Melodic Tom': 117,
    'Synth Drum': 118,
    'Reverse Cymbal': 119,
    'Guitar Fret Noise': 120,
    'Breath Noise': 121,
    'Seashore': 122,
    'Bird Tweet': 123,
    'Telephone Ring': 124,
    'Helicopter': 125,
    'Applause': 126,
    'Gunshot': 127,
}
"""List of MIDI general-1 instruments and their corresponding codes."""


PERCUSSION = {
    'Acoustic Bass Drum': 34,
    'Bass Drum 1': 35,
    'Side Stick': 36,
    'Acoustic Snare': 37,
    'Hand Clap': 38,
    'Electric Snare': 39,
    'Low Floor Tom': 40,
    'Closed Hi Hat': 41,
    'High Floor Tom': 42,
    'Pedal Hi-Hat': 43,
    'Low Tom': 44,
    'Open Hi-Hat': 45,
    'Low-Mid Tom': 46,
    'Hi-Mid Tom': 47,
    'Crash Cymbal 1': 48,
    'High Tom': 49,
    'Ride Cymbal 1': 50,
    'Chinese Cymbal': 51,
    'Ride Bell': 52,
    'Tambourine': 53,
    'Splash Cymbal': 54,
    'Cowbell': 55,
    'Crash Cymbal 2': 56,
    'Vibraslap': 57,
    'Ride Cymbal 2': 58,
    'Hi Bongo': 59,
    'Low Bongo': 60,
    'Mute Hi Conga': 61,
    'Open Hi Conga': 62,
    'Low Conga': 63,
    'High Timbale': 64,
    'Low Timbale': 65,
    'High Agogo': 66,
    'Low Agogo': 67,
    'Cabasa': 68,
    'Maracas': 69,
    'Short Whistle': 70,
    'Long Whistle': 71,
    'Short Guiro': 72,
    'Long Guiro': 73,
    'Claves': 74,
    'Hi Wood Block': 75,
    'Low Wood Block': 76,
    'Mute Cuica': 77,
    'Open Cuica': 78,
    'Mute Triangle': 79,
    'Open Triangle': 80,
}
"""List of MIDI general-1 percussion instruments and their corresponding codes.
To use, add a note to channel 9 with the pitch being the desired instrument."""    