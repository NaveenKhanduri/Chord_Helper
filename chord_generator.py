from scale_generator import *
import numpy as np



#returns the notes, in list format, that comprise a given chord. NAmes are given as 
class chord_shape:

    def __init__(self, chord_name = None):

        self.chord_name = chord_name
        self.notes = all_scales.notes 
        self.keys = scale_generator().all_keys
        self.shapes = ['6', 'm6', '7', 'maj7', 'm7', 'm7b5', '9','add9', 'madd9', 'maj9', 'm9', '11', 'm11', '13', 'maj13', 'm13', 'sus4', 'sus2', 'aug', '']
        self.base_chord = [1,3,5]
        
    #eventually nest this in a try except statement. 
    def chord(self):
        notes = self.notes
        base = [1,3,5]
        chord = []
        values = self.chord_name.split(' ') #better method should be used. Maybe a tuple?
        root = values[0]
        scale = scale_generator(root, 'major').scale()
        position = transpose(scale).transpose()  #maps the note sequence from scale to all notes, so it can 
        maj_7 = scale[6]
        maj_9 = scale[1]
        maj_11 = scale[3]
        maj_13 = scale[5]

        try:
            flat_3 = notes[position[scale[2]] - 1]

        except:
            flat_3 = notes[len(notes) - 1]
        try:
            flat_5 = notes[position[scale[4]] - 1]
        except:
            flat_5 = notes[len(notes) - 1]
        try:
            flat_7 = notes[position[scale[6]] - 1]
        except:
            flat_7 = notes[len(notes) - 1]
        try:
            sharp_5 = notes[position[scale[4]] + 1]
        except:
            sharp_5 = notes[0]
        #sharp_9 = position[position.index(scale[1]) + 1]
        #sharp_11 = position[position.index(scale[3]) + 1]

        for b in base:
            chord.append(scale[b-1])

        if len(values) <= 1:
            return chord
           
        elif 'sus2' in values[1]:
            second = scale[1]
            chord[1] = second
            return chord                

        elif 'sus4' in values[1]:
            fourth = scale[3]
            chord[1] = fourth
            return chord

        elif 'dim' in values[1]:
            chord[1] = flat_3
            chord[2] = flat_5

            if '7' in values[1]:
                chord.append(maj_13)
            return chord
            
        elif 'maj' in values[1]:  #covers maj variations first, then minor variations, then the rest
            var = values[1]
            if '7' in var:
                chord.append(maj_7)
            elif '9' in var:
                chord = chord + [maj_7, maj_9]
            elif '11' in var:
                chord = chord + [maj_7, maj_9, maj_11]
            else:
                chord = chord + [maj_7, maj_9, maj_11, maj_13]
            return chord
        
        elif 'm' in values[1]:  #covers the minor chords
            var = values[1]
            chord = [scale[0], flat_3, scale[4]]  

            if values[1] is 'm':
                return chord
            else:
                if '6' in var:
                    chord.append(scale[5])
                else:
                    if '7' in var:
                        if 'b5' in var:
                            chord[2] = flat_5
                            chord.append(flat_7)                       
                        else:
                            chord.append(flat_7)
                    elif 'add9' in var:
                        chord.append(maj_9)
                        return chord
                    elif '9' in var:
                        chord = chord + [flat_7, maj_9]
                    elif '11' in var:
                        chord = chord + [flat_7, maj_9, maj_11]                       
                    else:
                        chord = chord + [flat_7, maj_9, maj_11, maj_13]
            return chord
            
        elif '7' in values[1]:
            chord.append(flat_7)
            return chord

        elif 'add9' in values[1]:
            chord.append(maj_9)
            #print('add9')
            return chord

        elif '9' in values[1]:
            chord = chord + [flat_7, maj_9]
            #print('9')
            return chord
        elif '11' in values[1]:
            chord = chord + [flat_7, maj_9, maj_11]
            return chord
        elif '13' in values[1]:
            chord = chord + [flat_7, maj_9, maj_11, maj_13]
            return chord
        elif 'aug' in values[1]:
            chord[2] = sharp_5
            return chord
        else:           
            return chord


#the chord_sequencer class is initialized with the scale generator class. returns chord structure sequence. main class: sequence(self)
#inherit sequences from scale_sequences class when things get sorted out
#this class reutnrs a list of all the chords in a given scale
class chord_sequencer:


    def __init__(self, scale):
        try:
            self.scale = scale.scale()
            self.key = scale.key
            self.pattern = sequences [self.key]

        except:
            self.pattern = sequences ['major']

    def sequence(self):

        scale = self.scale
        chord_sequence = []
        pattern = self.pattern

        try:
            for i in range(len(pattern)):
                chord_sequence.append(scale[i] + pattern[i])
            return chord_sequence

        except:
            print("Sorry, the scale is not in the chord registry!")
            return None

#dataframe of all possible chord sequences for each scale and mode
class all_chord_sequences:
    sequences = sequences
    notes = all_scales.notes
    all_scales = {}
    
    for note in notes:
        note_dict = {}
        for key in sequences.keys():
            mode = f'{note} {key}'
            scale = scale_generator(note, key)
            note_dict[mode] = chord_sequencer(scale).sequence()
        all_scales[note] = note_dict


#references chord_sequencer class and instantiated with scale_generator class.
#highly specific, and only returns explicit chord progressions for a given scale that have been defined in the class. Meant as a base test for future models training
class chord_progression:
    full_circle = [1,4,7,3,6,2,5,1]
    circle = [1,4,5,1]
    full_circle = [1,4,7,3,6,2,5,1]
    circle = [1,4,5,1]
    blues_progression = [1,1,1,1,4,4,1,1,5,4,1,1]
    jazz_basic = [2,5,1]

    def __init__(self, scale):
        self.scale = scale
        self.chord_sequence = chord_sequencer(scale).sequence()

    def input_pattern(self, input):
        chords = {}
        chord_sequence = self.chord_sequence
        for c in input:
            try:
                chord = chord_sequence[c - 1]
                chords[chord] = chord_shape(chord).chord()
            except:
                chords[chord_sequence[c - 1]] = None
        return chords

    def all_chords(self):
        chord_shapes = {}
        for c in self.chord_sequence:
            try:
                chord_shapes[c] = chord_shape(c).chord()
            except:
                chord_shapes[c] = None
        return chord_shapes

    def full_circle(self):
        full_circle = self.full_circle
        chords = {}
        chord_sequence = self.chord_sequence
        for c in full_circle:
            try:
                chord = chord_sequence[c - 1]
                chords[chord] = chord_shape(chord).chord()
            except:
                chords[chord_sequence[c - 1]] = None
        return chords

    def circle(self):
        circle = self.circle
        chords = {}
        chord_sequence = self.chord_sequence
        for c in circle:
            try:
                chord = chord_sequence[c - 1]
                chords[chord] = chord_shape(chord).chord()
            except:
                chords[chord_sequence[c - 1]] = None
        return chords        

    def riff(self, chord_progression):
        progression = []
        for c in chord_progression:
            progression.append(self.chord_sequence[c - 1])
        return progression

