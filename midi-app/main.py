import random
from copy import deepcopy
from typing import Tuple

from midiutil import MIDIFile

from utils.music.constants import PROGRESSIONS, CHORDS, BASELINES, INSTRUMENTS
from utils.music import Melody, Scale, Note
from utils.constants import PATH_TO_OUTPUT
from utils import open_output


def generate_song(index=0, input_key=50, resolve=False, major_or_minor='minor',
                  total_repeats=1, baseline=None) -> Tuple[Melody, Melody]:
    """A function to randomly generate a melody.
    Returns a tuple of a list of melody notes and a list of chord notes.
    """

    # Define constants
    time_signature = 4
    beat_constant = 2
    key = input_key
    
    chords = Melody()
    melodies = Melody()
    
    # Duration model constants
    duration_model = list()
    duration_model_weight = 25  # DEFAULT : 25
    duration_model_init = {0.5: 2, 1.0: 3, 2.0: 2}
    
    # Pitch model constants
    pitch_model = list()
    pitch_model_weight = 1500  # DEFAULT : 1500
    pitch_model_init = [120, 20, 120, 20, 50, 2, 0, 0]
    
    # Chord model constants
    chord_model = list()
    chord_weight_rand = 78  # DEFAULT : 78
    chord_weight_deviation = 3  # DEFAULT : 3

    # Create chord progression
    resolution = ''
    while resolution != major_or_minor:
        progression_key = random.choice(list(PROGRESSIONS.keys()))
        progression, resolution = PROGRESSIONS[progression_key]
        
    progression_length = len(progression)

    # Print information
    print()
    print('Melody #' + str(index))
    print('Progression :    ' + progression_key)

    # Loop through measures
    for tr in range(total_repeats):
        for measure, chord in enumerate(progression):
            measure += tr*progression_length
            
            # Define constants
            time = measure * time_signature
            position = chord.position + key
            
            # -------------
            # Baseline
            # -------------
    
            # Generate baseline
            # melody = Melody(end_time=time + time_signature)
            melody = Melody(start_time=time, end_time=time + time_signature)
            baseline_list = chord.chord

            for note_position, time_position in baseline[0]:
                
                # Normalize note position
                octave = note_position // (len(baseline_list)) + baseline[2] - 0
                note_position %= (len(baseline_list))
                note_position = abs(note_position)
                
                # Find pitch
                pitch = baseline_list[note_position] + octave*12 + position
                
                # Find length
                if baseline[1] < 0:
                    base_length = time_signature
                else:
                    base_length = baseline[1]
                
                # melody.add(Note(pitch, time + time_position, base_length))
                melody.add(Note(pitch, time + time_position, base_length), update_times=False)
                # melody += Note(pitch, time + time_position, base_length)

            chords += melody
            # chords.end_time = melody.end_time
            # chords.add(melody, update_times=False)
            
            # -------------
            # Melody
            # -------------
    
            # Generate melody
            melody = Melody(start_time=measure * time_signature,
                            end_time=measure * time_signature + time_signature)
            scale = Scale(0, chord.scale)
    
            # While melody is not a measure long
            previous_duration = float('inf')
            note_index = 0
            was_chord = False
            # while not melody.chop(measure * time_signature + time_signature):
            while not melody.cut_to_length():

                # Obtain duration probabilities
                duration_dict = deepcopy(duration_model_init)
                
                # Obtain duration from model if not first measure
                if measure != 0:
                    if note_index < len(duration_model):
                        model_duration = duration_model[note_index]
                        duration_dict[model_duration] += duration_model_weight
                
                # Set duration
                found_duration = False
                while not found_duration:
                    
                    # Make durations from dict
                    durations = list()
                    for dur in duration_dict:
                        amount = duration_dict[dur]
                        for _ in range(amount):
                            durations.append(dur)
                    
                    # Randomize duration
                    duration = random.choice(durations)
                    
                    # Keep melodies on the beat
                    if duration <= previous_duration:
                        found_duration = True
                        previous_duration = duration
                        if time % beat_constant == 0:
                            previous_duration = float('inf')  # Largest
    
                # Setup movements
                scale_weights = deepcopy(pitch_model_init)
                
                if measure != 0:
                    if note_index < len(pitch_model):
                        model_pitch = pitch_model[note_index]
                        scale_weights[model_pitch] += pitch_model_weight
                
                movements = []
                for i, weight in enumerate(scale_weights):
                    movements += [i for _ in range(weight)]
    
                # Randomize movement
                index = random.choice(movements)
    
                # Find pitch in scale
                pitch = position + scale[index] + 12
                
                melody_chord = False
                
                # Init duration/pitch/chord model
                def chord_top():
                    return random.randint(chord_weight_rand - chord_weight_deviation, 
                                          chord_weight_rand + chord_weight_deviation)
                
                if measure == 0:
                    duration_model.append(duration)
                    pitch_model.append(index)
                    
                    chord_rand = random.randint(0, 100)
                    chord_model.append(chord_rand)
                    
                    if chord_rand > chord_top():
                        melody_chord = True
                        
                else:
                    if note_index < len(chord_model):
                        model_chord_rand = chord_model[note_index]
                        if model_chord_rand > chord_top():
                            melody_chord = True

                # Add note
                # melody.add(Note(pitch, time, duration))
                melody.add(Note(pitch, time, duration), update_times=False)
                # melody += Note(pitch, time, duration)
                
                if melody_chord and not was_chord:
                    was_chord = True
                else:
                    time += duration
                    was_chord = False
                note_index += 1

            # Add melody to melodies
            melodies.add(melody, update_times=True)
            # melodies += melody
            # melodies.end_time = melody.end_time

    # Fix long note issues by making notes end very slightly before the beat
    for note in melodies:
        note.duration -= 0.01

    # Resolve
    if resolve:
        melody = Melody(end_time=time_signature)
        resolve_chord = CHORDS[resolution]
        
        for i in range(0, 2):
            for note_position in resolve_chord:
                # melody.add(Note(key + note_position + i*12, 0, time_signature))
                melody += Note(key + note_position + i*12, 0, time_signature)
            
        melody = melody.retime(chords.end_time)
        
        chords += melody
        # chords.end_time += melody.end_time
        # melodies.end_time = chords.end_time

    # Print information
    print('Duration Model : ' + str(duration_model))
    print('Pitch Model :    ' + str(pitch_model))
    print('Chord Model :    ' + str(chord_model))
    print()

    return melodies, chords


def create_section_structure(min_melodies, max_melodies, dup):
    """A function to randomly generate the order of melodies.
    Returns a list of melody indices played in order.
    """

    # Determine total melodies
    melody_count = random.randint(min_melodies, max_melodies) - 1

    section_structure = list()
    current_melody = 0

    # While there are melodies left to generate
    while current_melody < melody_count:

        # Duplicate a past melody
        if random.random() < dup and current_melody > 1:
            random_index = random.randint(0, current_melody - 1)
            section_structure.append(random_index)

        # New melody
        else:
            section_structure.append(current_melody)
            current_melody += 1

    # Add resolving melody
    section_structure.append(melody_count)

    return section_structure


@open_output
def write_song() -> None:
    """Generates a song using the rule-based system."""

    # Define constants
    chord_track = 1
    melody_track = 0
    bass_instrument = random.choice([
        'Acoustic Grand Piano', 'Celesta'
    ])
    melody_instrument = random.choice([
        'Acoustic Grand Piano', 'Bright Acoustic Piano',
        'Electric Grand Piano', 'Electric Piano 1',
    ])
    bpm = random.randint(100, 200)
    key = random.randint(40, 55)
    mm = random.choice(['major', 'minor'])

    repeats = 2
    min_melodies, max_melodies = 2, 4
    melody_duplication = 0.5

    # Create section structure
    section_structure = create_section_structure(min_melodies, max_melodies, melody_duplication)
    print(section_structure)

    # Pick baseline
    baseline_key = random.choice(list(BASELINES.keys()))
    baseline = BASELINES[baseline_key]

    # Load MIDI file
    file = MIDIFile(2)

    # Assign tracks and instruments
    file.addTrackName(melody_track, 0, 'Melody')
    file.addTrackName(chord_track, 0, 'Bass Line')

    file.addProgramChange(0, melody_track, 0, INSTRUMENTS[melody_instrument])
    file.addProgramChange(0, chord_track, 0, INSTRUMENTS[bass_instrument])
    file.addTempo(0, 0, bpm)

    # Generate chords/melodies
    def gen(index, resolve=False):
        return generate_song(index=index, input_key=key, resolve=resolve, major_or_minor=mm,
                             total_repeats=repeats, baseline=baseline)

    # Print information
    print('Melody Instrument : ' + melody_instrument)
    print('Bass Instrument :   ' + bass_instrument)
    print('Key :               ' + mm)
    print('Baseline :          ' + baseline_key)

    section_list = list()

    # Create section types
    for i in range(max(section_structure) + 1):
        resolve = i == max(section_structure)
        section_list.append(gen(i + 1, resolve=resolve))

    melodies, chords = Melody(), Melody()

    # Generate final melody lists
    first = True
    for repeated_section in section_structure:
        section_melody, section_chords = section_list[repeated_section]

        # If the first addition to melodies
        if first:
            first = False
            melodies = section_melody
            chords = section_chords

        # If not the first addition to melodies
        else:
            # melodies.combine(section_melody)
            # chords.combine(section_chords)
            melodies += section_melody
            chords += section_chords

    # Remove duplicates
    for i1, note1 in enumerate(melodies.notes):
        for i2, note2 in enumerate(melodies.notes):
            if i1 != i2:
                if note1.pitch == note2.pitch and \
                        note1.time == note2.time:
                    melodies.notes.pop(i2)

    # Write chords and melodies to file
    # chords.set_track(chord_track)
    # chords.set_channel(chord_track)
    # chords.set_volume(50)
    chords.track = chord_track
    chords.channel = chord_track
    chords.volume = 50
    chords.write_to(file)

    # melodies.set_track(melody_track)
    # melodies.set_channel(melody_track)
    # melodies.set_volume(75)
    melodies.track = melody_track
    melodies.channel = melody_track
    melodies.volume = 75
    melodies.write_to(file)

    # Save song
    with open(PATH_TO_OUTPUT, 'wb') as output_file:
        file.writeFile(output_file)


if __name__ == '__main__':
    write_song()
