import unittest
from .util.melody import Melody
from .util.progression import Progression
from .util.scale import Mode
from .util.note import Note
from .util.scale import Scale

class NoteTest(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            Note(position=-0.1)
            
            
class ScaleTest(unittest.TestCase):
    def test_get(self):
        scale = Scale(Mode.Ionian)
        self.assertEquals(scale[-7], -12)
        self.assertEquals(scale[-6], -10)
        self.assertEquals(scale[-5], -8)
        self.assertEquals(scale[-4], -7)
        self.assertEquals(scale[-3], -5)
        self.assertEquals(scale[-2], -3)
        self.assertEquals(scale[-1], -1)
        self.assertEquals(scale[0], 0)
        self.assertEquals(scale[1], 2)
        self.assertEquals(scale[2], 4)
        self.assertEquals(scale[3], 5)
        self.assertEquals(scale[4], 7)
        self.assertEquals(scale[5], 9)
        self.assertEquals(scale[6], 11)
        self.assertEquals(scale[7], 12)
        self.assertEquals(scale[8], 14)
        self.assertEquals(scale[9], 16)
        self.assertEquals(scale[10], 17)
        self.assertEquals(scale[11], 19)
        self.assertEquals(scale[12], 21)
        self.assertEquals(scale[13], 22)
        self.assertEquals(scale[14], 23)
        

class MelodyTest(unittest.TestCase):
    
    def test_init(self):
        with self.assertRaises(ValueError):
            Melody(p_range=(3, 0))
        with self.assertRaises(ValueError):
            Melody(d_range=(1, -2))
    
    def test_generate(self):
        melody = Melody()
        with self.assertRaises(AssertionError):
            melody.generate(length=0)
        with self.assertRaises(AssertionError):
            melody.generate(epsilon=-0.1)
            
    def test_populate(self):
        melody = Melody()
        with self.assertRaises(AssertionError):
            melody.populate_notes(pos_offset=-1)
            
            
class ProgressionTest(unittest.TestCase):
    
    def test_generate_from_one(self):
        progression = Progression()
        melody = Melody()
        with self.assertRaises(AssertionError): # test non-generated melody
            progression.generate_from_one(melody=melody)
            
        melody.generate()
        with self.assertRaises(AssertionError):
            progression.generate_from_one(melody=melody, tone=Mode.Phrygian)
        with self.assertRaises(AssertionError):
            progression.generate_from_one(melody=melody, length_range=(0, 0))
        with self.assertRaises(AssertionError):
            progression.generate_from_one(melody=melody, length_range=(3, 2))