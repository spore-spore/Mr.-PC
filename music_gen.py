from transformers import AutoTokenizer, TransfoXLLMHeadModel, TransfoXLConfig, TransfoXLTokenizer, Trainer, TrainingArguments
import torch
from torch.utils.data import TensorDataset, DataLoader

from tokenizers import Tokenizer, models, pre_tokenizers, decoders

import music21 as m21
from music21 import instrument, note, chord

from schord_decoder import to_pitch, to_chord

config = TransfoXLConfig()
config.eos_token_id=0
config.pad_token_id=2

tokenizer = AutoTokenizer.from_pretrained("C:/Users/ibass/OneDrive/Desktop/Important Things/Git/music_creator/vocab_files")
tokenizer.eos_token = "<eos>"
tokenizer.pad_token = "<pad>"

model = TransfoXLLMHeadModel(config)
model.load_state_dict(torch.load('C:/Users/ibass/OneDrive/Desktop/Important Things/Git/music_creator/outputs/pytorch_model.bin',map_location=torch.device('cpu')))
model.eval()

seed_text = ""
num_tokens = 256

grammar = 1

#Full chorus of Autumn Leaves (long generation)
#chord_prog = ["C:min7","F:7","Bb:maj7","Eb:maj7","A:hdim7","D:7(b9)","G:min7","G:7(b9)","C:min7","F:7","Bb:maj7","Eb:maj7","A:hdim7","D:7(b9)","G:min7","G:min7","A:hdim7","D:7(b9)","G:min7","G:min7","C:min7","F:7","Bb:maj7","Eb:maj7","A:hdim7","D:7(#9)","G:min7","C:7","F:min7","Bb:7","Eb:7","A:hdim7","D:7(b9)","G:min7","G:7(b9)"]

chord_prog = ["A:hdim7", "D:7(b9)", "G:min7"]
chord_change_speed = 2
pos = 0
rhyth_pos = 0
seed_text = to_chord(chord_prog[0])

while pos < len(chord_prog):
    if grammar == 3:
        seed_text = seed_text + " " + to_chord(chord_prog[pos])
        grammar = 1
    else:
        length = len(seed_text.split())

        tokenized_seed = tokenizer.encode(seed_text, return_tensors="pt")

        if grammar == 1:
            generated_text = model.generate(tokenized_seed, max_length = length+1, do_sample=True, temperature = 0.5, min_length = length+1, top_p=0.92, top_k=50)
        elif grammar == 2:
            generated_text = model.generate(tokenized_seed, max_length = length+1, do_sample=True, temperature = 0.85, min_length = length+1, top_p=0.92, top_k=50)
            if generated_text[-2:] == "d4":
                generated_text = generated_text[:-2] + "d6"
        #print(generated_text)
        print(pos)

        new_text = tokenizer.decode(generated_text[0])
        finder = new_text.split()
        if finder[len(finder)-1].find('d') != -1 and finder[len(finder)-1].find('g') == -1:
            rhyth_pos += int(finder[len(finder)-1][1:])
        if rhyth_pos >= 96*chord_change_speed:
            rhyth_pos -= 96*chord_change_speed
            pos +=1

        seed_text = new_text
        grammar = grammar + 1

print("Seed text: ", seed_text)
print("Generated text: ", new_text)

def create_midi_long(gen):
    offset = 0
    output_notes = []
    gen = gen.split()
    count = 0
    restNow = False
    for pattern in gen:
        if (count % 3 + 1 == 1):
            count += 1
            continue
        elif (count % 3 + 1 == 2):
            if pattern.find('d') != -1 or len(pattern) > 3:
                count += 2
                continue
            elif pattern == '128':
                count += 1
                restNow = True
                continue
            new_note = note.Note(to_pitch(int(pattern)))
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            count += 1
        else:
            if pattern == 'dg':
                count += 1
                restNow = False
                continue
            elif restNow:
                count += 1
                dur = float(pattern[1:])/24.0
                offset += dur
                restNow = False
                continue
            dur = float(pattern[1:])/24.0
            new_note.duration.quarterLength = dur
            output_notes.append(new_note)

            offset += dur
            print(str(offset))
            count += 1

    midi_stream = m21.stream.Stream(output_notes)

    midi_stream.write('midi', fp='C:/Users/ibass/OneDrive/Desktop/Important Things/Git/music_creator/music/test_output_long.mid')

create_midi_long(new_text)