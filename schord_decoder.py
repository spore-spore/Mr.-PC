from enum import Enum
import json as j
from pathlib import Path

class Note(Enum):
    C = 0
    Db = 1
    D = 2
    Eb = 3
    E = 4
    F = 5
    Gb = 6
    G = 7
    Ab = 8
    A = 9
    Bb = 10
    B = 11

def to_chord(chordo):
    # # Opening JSON file
    # f = open(ann_path)
  
    # # returns JSON object as 
    # # a dictionary
    # data = j.load(f)

    # chord_bits = []
  
    # Iterating through the json
    # list
    #for i in data["notes"]:
        bit_vec = [0] * 12
        #curr = i["chord_changes"]["0"]

        split = chordo.split(":")
        root = split[0]

        shift = 0
        if root.find('#') != -1:
            root = root[0]
            shift = 1
        elif root.find('b') != -1:
            root = root[0]
            shift = -1
        root_val = Note((Note[root].value + shift) % 12).name
        root_val = Note[root_val]

        bit_vec[root_val.value] = 1
        
        # MINOR CHORDS
        if split[1].find('min') != -1:
            bit_vec[(root_val.value + 3) % 12] = 1 # b3
            bit_vec[(root_val.value + 7) % 12] = 1 # 5
            # minor 13 chords
            if split[1].find('min13') != -1:
                bit_vec[(root_val.value + 10) % 12] = 1 # b7
                bit_vec[(root_val.value + 2) % 12] = 1 # 9
                bit_vec[(root_val.value + 5) % 12] = 1 # 11, b3 and 11 are fine
                bit_vec[(root_val.value + 9) % 12] = 1 # 13
            # minor 11 chords
            if split[1].find('min11') != -1:
                bit_vec[(root_val.value + 10) % 12] = 1 # b7
                bit_vec[(root_val.value + 2) % 12] = 1 # 9
                bit_vec[(root_val.value + 5) % 12] = 1 # 11
            # minor 9 chords
            if split[1].find('min9') != -1:
                bit_vec[(root_val.value + 10) % 12] = 1 # b7
                bit_vec[(root_val.value + 2) % 12] = 1 # 9
            if split[1].find('7') != -1:
                # minmaj7 chords
                if split[1].find('maj') != -1:
                    bit_vec[(root_val.value + 11) % 12] = 1 # 7
                # min7 chords
                else:
                    bit_vec[(root_val.value + 10) % 12] = 1 # b7
        # MAJOR CHORDS
        elif split[1].find('maj') != -1:
            bit_vec[(root_val.value + 4) % 12] = 1 # 3
            bit_vec[(root_val.value + 7) % 12] = 1 # 5
            # major 13 chords (omit the 11 because natural 3 and 11 clash)
            if split[1].find('maj13') != -1:
                bit_vec[(root_val.value + 11) % 12] = 1 # 7
                bit_vec[(root_val.value + 2) % 12] = 1 # 9
                bit_vec[(root_val.value + 9) % 12] = 1 # 13
            # major 11 chords
            if split[1].find('maj11') != -1:
                bit_vec[(root_val.value + 11) % 12] = 1 # 7
                bit_vec[(root_val.value + 2) % 12] = 1 # 9
                bit_vec[(root_val.value + 5) % 12] = 1 # 11
            # major 9 chords
            if split[1].find('maj9') != -1:
                bit_vec[(root_val.value + 11) % 12] = 1 # 7
                bit_vec[(root_val.value + 2) % 12] = 1 # 9
            # major 7 chords
            if split[1].find('7') != -1:
                bit_vec[(root_val.value + 11) % 12] = 1 # 7
        # DIMINISHED CHORDS
        elif split[1].find('dim') != -1:
            bit_vec[(root_val.value + 3) % 12] = 1 # b3
            bit_vec[(root_val.value + 6) % 12] = 1 # b5
            # diminished 11 chord (no dim13, since bb7 == 6)
            if split[1].find('dim11') != -1:
                bit_vec[(root_val.value + 2) % 12] = 1 # 9
                bit_vec[(root_val.value + 5) % 12] = 1 # 11
                # half-diminished 11 chord
                if split[1].find('h') != -1:
                    bit_vec[(root_val.value + 10) % 12] = 1 # b7
                else:
                    bit_vec[(root_val.value + 9) % 12] = 1 # bb7
            # diminished 9 chord
            if split[1].find('dim9') != -1:
                bit_vec[(root_val.value + 2) % 12] = 1 # 9
                # half-diminished 9 chord
                if split[1].find('h') != -1:
                    bit_vec[(root_val.value + 10) % 12] = 1 # b7
                else:
                    bit_vec[(root_val.value + 9) % 12] = 1 # bb7
            # diminished 7 chord
            if split[1].find('dim7') != -1:
                # half-diminished 7 chord
                if split[1].find('h') != -1:
                    bit_vec[(root_val.value + 10) % 12] = 1 # b7
                else:
                    bit_vec[(root_val.value + 9) % 12] = 1 # bb7
        # DOMINANT CHORDS
        # dominant 7
        elif split[1][0] == ('7'):
            bit_vec[(root_val.value + 4) % 12] = 1 # 3
            bit_vec[(root_val.value + 7) % 12] = 1 # 5
            bit_vec[(root_val.value + 10) % 12] = 1 # b7
        # dominant 9
        elif split[1][0] == ('9'):
            bit_vec[(root_val.value + 4) % 12] = 1 # 3
            bit_vec[(root_val.value + 7) % 12] = 1 # 5
            bit_vec[(root_val.value + 10) % 12] = 1 # b7
            bit_vec[(root_val.value + 2) % 12] = 1 # 9
        # dominant 11 (3 is often omitted)
        elif split[1][0] == ('11'):
            bit_vec[(root_val.value + 7) % 12] = 1 # 5
            bit_vec[(root_val.value + 10) % 12] = 1 # b7
            bit_vec[(root_val.value + 2) % 12] = 1 # 9
            bit_vec[(root_val.value + 5) % 12] = 1 # 11
        # dominant 13 (11 is often omitted)
        elif split[1][0] == ('13'):
            bit_vec[(root_val.value + 4) % 12] = 1 # 3
            bit_vec[(root_val.value + 7) % 12] = 1 # 5
            bit_vec[(root_val.value + 10) % 12] = 1 # b7
            bit_vec[(root_val.value + 2) % 12] = 1 # 9
            bit_vec[(root_val.value + 9) % 12] = 1 # 13
        # major triad    
        else:
            bit_vec[(root_val.value + 4) % 12] = 1 # 3
            bit_vec[(root_val.value + 7) % 12] = 1 # 5

        # flat-9 alteration
        if split[1].find('(b9)') != -1:
            bit_vec[(root_val.value + 1) % 12] = 1

        # sharp-9 alteration
        if split[1].find('(#9)') != -1:
            bit_vec[(root_val.value + 3) % 12] = 1

        # flat-5 alteration
        if split[1].find('(b5)') != -1:
            bit_vec[(root_val.value + 6) % 12] = 1

        # sharp-five (augmented chord) == flat-13 alteration
        if split[1].find('(#5)') != -1 or split[1].find('(b13)') != -1:
            bit_vec[(root_val.value + 8) % 12] = 1

        # 6-chords
        if split[1].find('6') != -1:
            bit_vec[(root_val.value + 9) % 12] = 1

        # (9) is used to express 6/9 chords
        if split[1].find('(9)') != -1:
            bit_vec[(root_val.value + 2) % 12] = 1

        # chord_bits.append(bit_vec)

    # Closing file
    # f.close()

        strrep = ""

        for i in bit_vec:
            strrep = strrep + str(i)

        return strrep
        # return bit_vec

def to_pitch(midi):
    root_val = str(Note(midi % 12).name)
    if root_val.find('b') != -1:
        new_val = root_val[0]
        new_val = new_val + '-'
        root_val = new_val

    reg = midi // 12 - 1
    root_val = root_val + str(reg)
    return root_val

print(to_pitch(55))