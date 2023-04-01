import music21 as m21
import numpy as np
import os
from schord_decoder import to_chord
import json as j

# 8 measures
#PHRASE_LENGTH = 768
# 4 measures
#PHRASE_LENGTH = 384
# 2 measures
PHRASE_LENGTH = 192

# Only use a portion of the data = 1/FRAC it's actual size
FRAC = 8

def calculate_rest(note2start, note1start, note1duration, bar1, bar2):
  return note2start + (96 * (bar2 - bar1)) - (note1start + note1duration)

# root_path = "C:/Users/ibass/OneDrive/Desktop/Important Things/Git/thesis-contents/midi_files"

# files = os.listdir(root_path)

# notes = []

# note_len = []

# print(len(files))

# for i in range(0,int(len(files))):

#   lol = 0

#   m = m21.midi.MidiFile()
#   parsed = m21.converter.parse(root_path+'/'+files[i])

#   notes_parser = parsed.flat.notes

#   for element in notes_parser:
#             if isinstance(element, m21.note.Note):
#                 pitch = str(element.pitch)
#                 octave = int(pitch[len(pitch) - 1])
#                 root = pitch[0]
#                 notes.append(pitch)
#                 lol = lol + 1
  
#   note_len.append(lol)

# n_vocab = len(set(notes))
# n_vocab = n_vocab - 1
# print(n_vocab)

# note_names = sorted(set(item for item in notes))
# print(note_names)

# note_map = dict((note, number) for number, note in enumerate(note_names))

# print(len(notes))

root_path_ann = "/home/christopherthompson/Desktop/thesis-contents/fixed_annotations"

annots = os.listdir(root_path_ann)

bits = []

ann_len = []

counter = 0

for i in range(0,int(len(annots))//FRAC):

  # Opening JSON file
  f = open(root_path_ann+'/'+annots[i])
  # print(root_path_ann+'/'+annots[i])
  
  # returns JSON object as 
  # a dictionary
  data = j.load(f)

  start = True

  prev_pos = 0
  prev_dur = 0
  now_pos = 0
  now_dur = 0
  prev_chord = 0
  now_chord = 0
  now_bar = 0
  prev_bar = 0


  for i in data["notes"]:
    
    now_chord = to_chord(i["chord_changes"]["0"])
    now_pos = i["s_rhythmic_position"]
    now_dur = i["s_rhythmic_duration"]
    now_bar = i["bar_num"]

    if start:
      rest = []
      if i["bar_num"] == 2 and i["s_rhythmic_position"] != 0:
        rest.append(now_chord)
        rest.append(128)
        rest.append(i["s_rhythmic_position"])
        bits.append(rest)
      start = False
    elif calculate_rest(now_pos, prev_pos, prev_dur, prev_bar, now_bar) > 0:
      rest = []
      if now_chord == prev_chord:
        rest.append(now_chord)
      else:
        rest.append(prev_chord)
      rest.append(128)
      rest.append(calculate_rest(now_pos, prev_pos, prev_dur, prev_bar, now_bar))
      bits.append(rest)


    midi = i["midi_pitch"]
    bit_vecs = []
    bit_vecs.append(now_chord)
    # bit_vecs.append(curr)
    bit_vecs.append(midi)
    if i["is_grace"] == 1:
      bit_vecs.append('g')
    else:
      bit_vecs.append(now_dur)

    bits.append(bit_vecs)

    prev_chord = now_chord
    prev_pos = now_pos
    prev_dur = now_dur
    prev_bar = now_bar
  
  f.close()

dur_counter = 0
all_data = []
data_string = ""

for i in bits:
  if i[2] != 'g':
    dur_counter = dur_counter + i[2]
  data_string = data_string+str(i[0])+' '
  data_string = data_string+str(i[1])+ ' '
  data_string = data_string+'d'+str(i[2]) #+' '
  #data_string = data_string+'<sep>' Removing sep token

  if dur_counter > PHRASE_LENGTH:
    all_data.append(data_string)
    all_data.append(" <eos>")
    all_data.append("\n")
    data_string = ""
    dur_counter = dur_counter - PHRASE_LENGTH
  else:
    data_string = data_string+' '

# print(all_data)

file1 = open("/home/christopherthompson/Desktop/thesis-contents/jazz_data.txt","a")
file1.writelines(all_data)
file1.close()

# for i in bits:
#   count = 0
#   for k in i:
#     if count == 2:
#       print('d'+str(k)+' ', end="")
#     else:
#       print(str(k)+' ', end="")
#     count = count + 1
#   print('<sep> ', end="")

#print(bits)
