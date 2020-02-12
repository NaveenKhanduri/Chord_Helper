import numpy as np 
import itertools
from collections import OrderedDict 

#when using the scale object in any class, define it as scale(root, key), not the actual function scale.scale()
#houses all available scale patterns
#base class - does not have parent classes
#all output is in the form of a list, not an array
class all_scales: 

    notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    keys = ['major', 'major_pentatonic', 'minor', 'minor_pentatonic', 'blues', 'dorian', 'mixolydian', 'lydian', 'locrian', 'phrygian', 'phrygian_dominant']

    #interval pattern, doubled (so a half step equals 1, a whole step equals 2)
    major = [2,2,1,2,2,2,1]
    major_pentatonic = [2,2,3,2,3]
    minor = [2,1,2,2,1,2,2]
    minor_pentatonic = [3,2,2,3,2]
    blues = [3,2,1,1,3,2]
    dorian = [2,1,2,2,2,1,2]
    mixolydian = [2,2,1,2,2,1,2]
    lydian = [2,2,2,1,2,2,1]
    locrian = [2,2,1,1,2,2,2]
    phrygian = [1,2,2,2,1,2,2]
    phrygian_dominant = [1,3,1,2,1,2,2]

    all_modes = [major, major_pentatonic, minor, minor_pentatonic, blues, dorian, mixolydian, lydian, locrian, phrygian, phrygian_dominant]

    unordered_keys = {}

    for i in range(len(all_modes)):
        unordered_keys[keys[i]] = all_modes[i]
    
    all_keys = OrderedDict(sorted(unordered_keys.items()))


#instantiated with root note name ('C', 'Eb', ect) and mode/key
#returns a list of all 7 root notes in a scale
class scale_generator:


    def __init__(self, root = None, key = None):
        self.notes = all_scales.notes
        self.all_keys = all_scales.all_keys
        self.root = root
        self.key = key
        try:
            self.pattern = self.all_keys[self.key]
        except:
            self.pattern = self.all_keys['major']

    def scale(self):
        notes = self.notes
        root = self.root
        try:
            pattern = self.pattern
        except:
            print('pattern not found')
        try:
            scale = [root]
            num = notes.index(root)
            for p in pattern:
                num += p
                if num < len(notes):
                    scale.append(notes[num])

                elif num == len(notes):
                    num = 0
                    scale.append(notes[num])
                else:
                    num = p - 1
                    scale.append(notes[num])
            return scale
        except:
            print("Please choose between: ", notes, "\n And keys:", self.all_keys)

#class housing list of chord sequences. Stored for potential debugging purposes, possibly not needed
'''
class scale_sequences:

    notes = all_scales.notes

    major_sequence = ['', ' m', ' m', '','',' m', ' dim']
    tenessee_sequence = ['', ' m', ' 7', '', ' 7', ' 6', '']
    pop_sequence = ['', ' m', ' 7', '', ' 7', ' m', '']
    pentatonic_major = ['', ' m', ' m', '', ' m']
    minor_sequence = [' m', ' dim', '', ' m', ' m', '', '']
    pentatonic_minor = [' m', '', ' m', ' m', '']
    lydian_sequence = ['','', ' m', ' dim', '', ' m', ' m']
    dorian_sequence = [' m',' m','','',' m',' dim','']
    mixolydian_sequence = ['', ' m', ' dim', '', ' m',' m','']
    blues_sequence = [' maj7', ' m7', ' m7', ' 7', ' 7', ' m7', ' dim7']
    phrygian_sequence = [' m', '', '', ' m', ' dim', '', ' m']
    phrygian_dominant_sequence = ['', '', ' dim', ' m', ' dim', '', '']
    jazz_sequence = [' maj7', ' m7', ' m7',  ' maj7', ' 7', ' m7', ' m7b5']

    sequences = OrderedDict({'major': major_sequence, 'major_pentatonic': pentatonic_major, 'minor': minor_sequence, 'minor_pentatonic': pentatonic_minor,\
        'lydian': lydian_sequence, 'dorian': dorian_sequence, 'mixolydian': mixolydian_sequence, 'blues': blues_sequence, 'tenessee': tenessee_sequence, 'pop': pop_sequence, \
       'phrygian': phrygian_sequence, 'phrygian_dominant': phrygian_dominant_sequence, 'jazz': jazz_sequence})
'''

notes = all_scales.notes    
major_sequence = ['', ' m', ' m', '','',' m', ' dim']
tenessee_sequence = ['', ' m', ' 7', '', ' 7', ' 6', '']
pop_sequence = ['', ' m', ' 7', '', ' 7', ' m', '']
pentatonic_major = ['', ' m', ' m', '', ' m']
minor_sequence = [' m', ' dim', '', ' m', ' m', '', '']
pentatonic_minor = [' m', '', ' m', ' m', '']
lydian_sequence = ['','', ' m', ' dim', '', ' m', ' m']
dorian_sequence = [' m',' m','','',' m',' dim','']
mixolydian_sequence = ['', ' m', ' dim', '', ' m',' m','']
blues_sequence = [' maj7', ' m7', ' m7', ' 7', ' 7', ' m7', ' dim7']
phrygian_sequence = [' m', '', '', ' m', ' dim', '', ' m']
phrygian_dominant_sequence = ['', '', ' dim', ' m', ' dim', '', '']
jazz_sequence = [' maj7', ' m7', ' m7',  ' maj7', ' 7', ' m7', ' m7b5']

unordered_sequences = OrderedDict({'major': major_sequence, 'major_pentatonic': pentatonic_major, 'minor': minor_sequence, 'minor_pentatonic': pentatonic_minor,\
    'lydian': lydian_sequence, 'dorian': dorian_sequence, 'mixolydian': mixolydian_sequence, 'blues': blues_sequence, 'tenessee': tenessee_sequence, 'pop': pop_sequence, \
    'phrygian': phrygian_sequence, 'phrygian_dominant': phrygian_dominant_sequence, 'jazz': jazz_sequence})  
sequences = OrderedDict(sorted(unordered_sequences.items()))


#maps notes in a scale to position along the one-octave notes list: map(scale[i]) -> notes[j]) in a dictionary format. Maybe function would be more useful
#Used for chord generator, so it can find the notes of a given chord
#only class that takes the scale.scale() function, not the scale class object, as its input. 
class transpose:

    def __init__(self, scale):
        self.scale = scale
        self.notes = all_scales.notes
    def transpose(self):
        transpose_index = {}
        for s in self.scale:
            transpose_index[s] = self.notes.index(s)
        return transpose_index
