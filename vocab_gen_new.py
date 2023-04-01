from transformers import AutoTokenizer, TransfoXLLMHeadModel
import tokenizers
from collections import OrderedDict

from pathlib import Path


paths = "/home/christopherthompson/Desktop/thesis-contents/jazz_data.txt"

old_tokenizer = AutoTokenizer.from_pretrained("transfo-xl-wt103")

text_file = open(paths, 'r')
text = text_file.read()

#cleaning
words = text.split()
words = [word.strip('\n') for word in words]
#trunc_list = slice(len(words)//16)
#words = words[trunc_list]
#print("HEYYYY2"+str(len(words)))

#finding unique
unique = []
unique.append("<eos>")
unique.append("<unk>")
unique.append("<pad>")
unique.append("<formula>")
for word in words:
    if word not in unique:
        unique.append(word)

sym_idx = OrderedDict((j,i) for i,j in enumerate(unique))

old_tokenizer.sym2idx = sym_idx
old_tokenizer.idx2sym = unique

old_tokenizer.save_pretrained("/home/christopherthompson/Desktop/thesis-contents/vocab_files")



















# text_file = open(paths, 'r')
# text = text_file.read()

# #cleaning
# words = text.split()
# words = [word.strip('\n') for word in words]
# #trunc_list = slice(len(words)//16)
# #words = words[trunc_list]
# #print("HEYYYY2"+str(len(words)))

# #finding unique
# unique = []
# unique.append("<bos>")
# unique.append("<eos>")
# unique.append("<unk>")
# unique.append("<pad>")
# for word in words:
#     if word not in unique:
#         unique.append(word)

# print(unique)

# lol = dict((j,i) for i,j in enumerate(unique))

# with open('jazz_vocab.txt', 'w') as fp:
#     for i in lol.items():
#         fp.write(str(i[0])+'\n')