from __future__ import annotations
from copy import copy, deepcopy
from dataclasses import dataclass
from typing import List, Optional, Iterable, Union, Callable, Any
import os
from functools import wraps

from midiutil import MIDIFile


__all__ = ['Note', 'Chord', 'Scale', 'Melody']

PATH_TO_OUTPUT = 'out/out.mid'

@dataclass
class Note:
    """Class to store information on Notes.

    Args:
        pitch: pitch of the note
        time: time at which the note is played in beats
        duration: duration the note is played in beats
        track: track the note belongs to
        channel: channel the note belongs to
        volume: volume of the note
        debug_output: used for testing duration issues
    """
    pitch: int
    time: float
    duration: float
    track: Optional[int] = None
    channel: Optional[int] = None
    volume: Optional[int] = 100

    def __iter__(self) -> Iterable:
        """Returns an iterable with values in the order needed to write to a
        file from the MIDIUtil library.

        Raises:
            AssertionError if the Note has parameters that are not initialized
            or invalid MIDI parameters
        """

        iterable = [self.track, self.channel, self.pitch, self.time,
                    self.duration, self.volume]

        # Test if note is valid
        assert all([val is not None for val in iterable]), \
            'Value was not initialized'
        assert 0 <= self.pitch <= 127, \
            f'{self.pitch} is not a valid MIDI pitch'

        return iter(iterable)


@dataclass
class Chord:
    """Class to store information on Chords.

    Args:
        chord: name of the chord
        scale: scale of the chord
        position: position of the chord
    """
    chord: List[int]
    scale: List[int]
    position: int


class Scale:
    def __init__(self, starting_note: int, scale: List[int]) -> None:
        """Creates a new Scale.

        Args:
            starting_note: the note to start on
            scale: distances between notes in half-steps
        """
        self.starting_note = starting_note
        self.differences = scale

    @property
    def scale(self) -> List[int]:
        """Returns a list of notes in the scale.

        Will be calculated based on starting_note and differences.
        """
        starting_note = self.starting_note
        scale_ = []
        for dif in self.differences:
            scale_.append(starting_note)
            starting_note += dif
        scale_.append(starting_note)
        return scale_

    def lower(self, octaves: int = 1) -> Scale:
        """Lowers the scale down an octave.

        Args:
            octaves: octaves to lower, if negative will raise the scale
        """
        return Scale(self.starting_note - 12 * octaves, self.differences)

    def __repr__(self) -> str:
        return f'Scale(starting_note={self.starting_note}, differences={self.differences}, scale={self.scale})'

    def __len__(self) -> int:
        return len(self.scale)

    def __getitem__(self, item: int) -> int:
        """Overrides default indexing. Only allows for one index. If the index
        is out of bounds, will raise or lower the scale to the desired
        position."""
        assert isinstance(item, int), 'Scale indexing only supports int'

        scale = self.scale

        # Extend scale if item is too big
        offset = 12
        while item >= len(scale) - 1:
            scale += [note + offset for note in scale][1:]
            offset += 12

        # Extend scale if item is too small
        offset = 12
        while item < 0:
            scale = [note - offset for note in scale][:-1] + scale
            offset += 12
            item += len(self)

        return scale[item]


class Melody:
    def __init__(self, start_time: float = 0, end_time: float = 0,
                 notes: Optional[List[Note]] = None) -> None:
        """Creates a new Melody.

        Args:
            start_time: the time the Melody starts at
            end_time: the time the Melody ends at
            notes: list of notes to use, if not specified will be empty
        """

        if notes is not None:
            self.notes = notes
        else:
            self.notes = []

        self.start_time = start_time
        self.end_time = end_time

    @property
    def duration(self) -> float:
        """the duration of the Melody"""
        return self.end_time - self.start_time

    def __iter__(self) -> Iterable[Note]:
        return iter(self.notes)

    def __len__(self) -> int:
        return len(self.notes)

    def __repr__(self) -> str:
        return f'Melody(start_time={self.start_time}, end_time={self.end_time}, {len(self)} notes)'

    def add(self, other: Union[Note, Melody],
            update_times: bool = True) -> None:
        """Adds a melody or a Note.

        Args:
            other: Melody or Note to add
            update_times: whether to update the end_time of the melody
        """

        if isinstance(other, Note):
            self.notes.append(other)
            if update_times:
                self.end_time = max(self.end_time, other.time + other.duration)

        elif isinstance(other, Melody):
            if update_times:
                other = other.retime(self.end_time)
                self.end_time += other.duration
            self.notes += other.notes

        else:
            raise TypeError('add can only be called with Melody or Note')

    def __add__(self, other: Union[Note, Melody]) -> Melody:
        """Wrapper for add method."""
        new_melody = deepcopy(self)
        new_melody.add(other)
        return new_melody

    def retime(self, new_start_time: float) -> Melody:
        """Retimes a Melody so all the Notes play as if the Melody was started
        at new_start_time."""

        retime_difference = new_start_time - self.start_time
        retimed = Melody(self.start_time + retime_difference,
                         self.end_time + retime_difference)

        for note in self:
            copied_note = copy(note)
            copied_note.time += retime_difference
            retimed.add(copied_note, update_times=False)

        return retimed

    def __mul__(self, other: int) -> Melody:
        """Extends a Melody by duplicating it a number of times."""
        assert isinstance(other, int), 'Melodies can only be multiplied by int'

        new_melody = deepcopy(self)
        for i in range(other - 1):
            new_melody += self

        return new_melody

    def cut_to_length(self, length: Optional[float] = None,
                      cut_on_duration: bool = True) -> bool:
        """Removes all Notes after length.

        Args:
            length: removes all Notes that play or finish playing after length.
                    if None, use the Melody's end_time
            cut_on_duration: whether to cut notes that start before length but
                             end after length

        Returns:
            False if no Notes were removed, True if Notes were removed
        """

        if length is None:
            length = self.end_time

        old_notes = self.notes
        if cut_on_duration:
            self.notes = [note for note in self.notes if
                          note.time + note.duration <= length]
        else:
            self.notes = [note for note in self.notes if
                          note.time <= length]
        return old_notes != self.notes

    def __setattr__(self, key: str, value: Any) -> None:
        """If volume, track, or channel are set it will automatically set all
        Notes in the Melody to match it. These do not have getters and support
        having different values, but is just an easy way to set defaults."""

        if key == 'volume':
            for note in self:
                note.volume = value

        elif key == 'track':
            for note in self:
                note.track = value

        elif key == 'channel':
            for note in self:
                note.channel = value

        else:
            super(Melody, self).__setattr__(key, value)

    def write_to(self, file: MIDIFile) -> None:
        """Write all Notes in the Melody to a MIDI file.

        Args:
            file: MIDI file to write to, from the MIDIUtil library
        """

        for note in self.notes:
            file.addNote(*tuple(note))
