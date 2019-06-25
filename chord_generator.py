import numpy as np
import itertools


#houses all available scale patterns
class all_scales: 

    notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    keys = ['major', 'major_pentatonic', 'minor', 'minor_pentatonic', 'blues', 'dorian', 'mixolydian', 'lydian', 'locrian']

    #interval pattern, doubled (so a half step equals 1, a whole step equals 2)
    major = [2,2,1,2,2,2,1]
    major_pentatonic = [2,2,3,2,3]
    minor = [2,1,2,2,1,2,2]
    minor_pentatonic = [3,2,2.3,2]
    blues = [3,2,1,1,3,2]
    dorian = [2,1,2,2,2,1,2]
    mixolydian = [2,2,1,2,2,1,2]
    lydian = [2,2,2,1,2,2,1]
    locrian = [2,2,1,1,2,2,2]

    all_modes = [major, major_pentatonic, minor, minor_pentatonic, blues, dorian, mixolydian, lydian, locrian]

    all_keys = {}

    for i in range(len(all_modes)):
        all_keys[keys[i]] = all_modes[i]

class scale_generator:
    notes = all_scales.notes
    all_keys = all_scales.all_keys

    def __init__(self, root = None, key = None):
        self.root = root
        self.key = key

    def scale(self):
        notes = scale_generator.notes
        key = self.key
        root = self.root
        pattern = scale_generator.all_keys[key]
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
            print("Please choose between: ", notes, "\n And keys:", scale_generator.keys)

#maps notes in a scale to position along the one-octave notes list: map(scale[i]) -> notes[j]
class transpose:
    notes = all_scales.notes
    def __init__(self, scale):
        self.scale = scale   
    def transpose(self):
        transpose_index = []
        for s in self.scale:
            transpose_index.append(transpose.notes.index(s))
        return transpose_index

#work in progress. Oh boy, this is gonna get a little complicated. For now, chord_name is read as the [root note + variation] (eg. C add9, F maj7, G, ect.)
class chord_shape:


    def __init__(self, chord_name = None):
        self.chord_name = chord_name

    notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    keys = scale_generator().all_keys
    shapes = ['6', 'm6', '7', 'maj7', 'm7', '9','add9', 'madd9', 'maj9', 'm9', '11', 'm11', '13', 'maj13', 'm13', 'sus4', 'sus2', 'aug', '']
    base_chord = [1,3,5]

    def chord(self):
        notes = chord_shape.notes
        base = [1,3,5]
        chord = []
        values = self.chord_name.split(' ')
        root = values[0]
        scale = scale_generator(root, 'major').scale()
        position = transpose(scale).transpose()

        maj_7 = scale[6]
        maj_9 = scale[1]
        maj_11 = scale[3]
        maj_13 = scale[5]
        try:
            flat_3 = notes[position.index(scale[2]) - 1]  #fix after testing
        except:
            flat_3 = notes[len(notes) - 1]
        try:
            flat_5 = notes[position.index(scale[4]) - 1]
        except:
            flat_5 = notes[len(notes) - 1]
        try:
            flat_7 = notes[position.index(scale[6]) - 1]
        except:
            flat_7 = notes[len(notes) - 1]
        try:
            sharp_5 = notes[position.index(scale[4]) + 1]
        except:
            sharp_5 = notes[0]
        #sharp_9 = position[position.index(scale[1]) + 1]
        #sharp_11 = position[position.index(scale[3]) + 1]

        for b in base:
            chord.append(scale[b-1])

        if len(values) <= 1:
            print('chord')
            return chord

            

        elif 'sus2' in values[1]:
            second = position.index(scale[1])
            chord[1] = position[second]
            #print('sus2')
            return chord                

        elif 'sus4' in values[1]:
            fourth = scale[3]
            chord[1] = fourth
            return chord
            
        elif 'maj' in values[1]:  #covers maj variations first, then minor variations, then the rest
            var = values[1]
            if '7' in var:
                chord.append(maj_7)
            elif '9' in var:
                chord = chord + [maj_7, maj_9]
                #print('maj9')
            elif '11' in var:
                chord = chord + [maj_7, maj_9, maj_11]
            else:
                chord = chord + [maj_7, maj_9, maj_11, maj_13]
            return chord
            

        
        elif 'm' in values[1]:  #covers the minor chords
            var = values[1]
            chord = [scale[0], flat_3, scale[4]]  

            if values[1] is 'm':
                #print('m')
                return chord
            else:
                if '6' in var:
                    chord.append(scale[5])
                else:
                    if '7' in var:                       
                        chord.append(flat_7)
                    elif 'add9' in var:
                        chord.append(maj_9)
                        #print('madd9')
                        return chord
                    elif '9' in var:
                        #print('m9')
                        chord = chord + [flat_7, maj_9]
                    elif '11' in var:
                        chord = chord + [flat_7, maj_9, maj_11]                       
                    else:
                        chord = chord + [flat_7, maj_9, maj_11, maj_13]
                        #print('m13')
            return chord

            

        elif 'dim' in values[1]:
            chord[1] = flat_3
            chord[2] = flat_5

            if '7' in values[1]:
                chord.append(maj_13)
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
                    
#the chord_generator class takes input from the scale_generator class. Planning on building a few helper classes for this one.
class chord_generator:
    major_sequence = [' ', ' m', ' m', ' ',' ',' m', ' dim']
    minor_sequence = [' m', ' dim', '', ' m', ' m', ' ', ' ']
    lydian_sequence = [' ',' ', ' m', ' dim', ' ', ' m', ' m']
    dorian_sequence = [' m',' m',' ',' ',' m',' dim',' ']
    mixolydian_sequence = [' ', ' m', ' dim', ' ', ' m',' m',' ']
    blues_sequence = [' maj7', ' m 7', ' m 7', ' 7', ' 7', ' m 7', ' dim 7']


    all_sequences = {'major': major_sequence, 'minor': minor_sequence, 'lydian': lydian_sequence, 'dorian': dorian_sequence, 'mixolydian': mixolydian_sequence, 'blues': blues_sequence}

    def sequence(scale):

        key = scale.key
        scale = scale.scale()
        chord_sequence = []
        try:
            pattern = chord_generator.all_sequences[key]
            for i in range(len(pattern)):
                chord_sequence.append(scale[i] + pattern[i])
            return chord_sequence
        except:
            print("Sorry, the scale is not in the chord registry!")

    def riff(scale, chord_progression):
        scale = scale.scale()
        progression = []
        for c in chord_progression:
            progression.append(scale[c - 1])
        return progression

 

#these will be put....somewhere........eventually        
full_circle = [1,4,7,3,6,2,5,1]
circle = [1,4,5,1]
blues_progression = [1,1,1,1,4,4,1,1,5,4,1,1]
jazz_basic = [2,5,1]




blues_scaleC = scale_generator('C', 'blues').scale()

lydian_fun = scale_generator('Eb', 'lydian')

chord = chord_shape('C add9').chord()

print(chord)