import music21 as m21
import numpy as np
import os
from schord_decoder import to_chord
import json as j

root_path_ann = "C:/Users/Christopher_Thompso1/Desktop/thesis/thesis-contents/annotation_files"
chord_path = "C:/Users/Christopher_Thompso1/Desktop/thesis/thesis-contents/chord_sheets"
final_path = "C:/Users/Christopher_Thompso1/Desktop/thesis/thesis-contents/fixed_annotations"

malformed = ["02", "04", "05", "12", "13", "14", "15", "20", "21", "23", "24", "29", "32", "33", "40", "44", "46"]
repeat_head =  [1, 1, 2, 2, 0, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1]
length_prof_solo = [1, 1, 3, 2, 1, 2, 1, 1, 1, 4, 1, 2, 2, 1, 2, 2, 2]
num_choruses = [2, 3, 7, 9, 6, 8, 7, 4, 2, 17, 7, 18, 10, 8, 6, 7, 6]

annots = os.listdir(root_path_ann)

bits = []

ann_len = []

counter = 0

for k in range(0,int(len(annots))):

  # Opening JSON file
  f = open(root_path_ann+'/'+annots[k])
  print(f)
  # print(root_path_ann+'/'+annots[i])
  
  # returns JSON object as 
  # a dictionary
  data = j.load(f)

  start = True

  # Determine which song this file is annotating and prepare to fix chords if it is one of the malformed songs
  song_number = str(annots[k])[(len(str(annots[k])) - 7):(len(str(annots[k]))-5)]
  file_open = "0"
  sheet = "0"
  loc = -1
  total_choruses = -1
  print(song_number)
  if song_number in malformed and song_number != "13" and song_number != "12":
    print(song_number+" is malformed")
    file_open = open(chord_path+"/"+song_number+".json")
    print(file_open)
    sheet = j.load(file_open)
    loc = malformed.index(song_number)
    total_choruses = repeat_head[loc] + length_prof_solo[loc] + num_choruses[loc]
    print("Num choruses: "+str(total_choruses))

    base_offset = data["notes"][0]["bar_num"]
    print("Base offset: "+str(base_offset),end=" ")

    in_coda = False
    count = 0

    # Begin looping through each note
    for i in range(0,len(data["notes"])):
        
        bar = data["notes"][i]["bar_num"] - base_offset-1
        if bar == -1:
            continue
        print("BAR: "+str(bar),end=" ")
        form_part = "Head"

        # Determine where in the form you are
        if isinstance(sheet, dict) and ("Intro" in sheet) and bar*4 + data["notes"][i]["s_rhythmic_position"] < int(sheet["Intro"]["Length"])*4:
            # In intro
            form_part = "Intro"
        elif ("Intro" in sheet):
            # Outside of intro
            bar = bar - int(sheet["Intro"]["Length"])

        chorus_num = bar / (int(sheet["Head"]["Length"])/4) + 1
        overall_pos = bar * 96 + data["notes"][i]["s_rhythmic_position"]
        quarter_pos = int(overall_pos / 24)
        form_pos = quarter_pos % (int(sheet["Head"]["Length"]))
        print("Now @"+str(form_pos))

        if chorus_num == total_choruses and not in_coda:
            if form_pos == int(sheet["Coda"]["Replace"]):
                in_coda = True

        if in_coda:
            form_part = "Coda"
            form_pos = form_pos - int(sheet["Coda"]["Replace"])

        print(str(int(form_pos)+1),end="")
        proper_chord = sheet[form_part][str(int(form_pos)+1)]

        data["notes"][i]["chord_changes"]["0"] = proper_chord

  if song_number != "13" and song_number != "12":
    with open(final_path+"/"+str(k)+".json", "w") as outfile:
        j.dump(data, outfile)
  
  f.close()