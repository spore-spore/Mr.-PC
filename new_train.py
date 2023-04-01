from transformers import AutoTokenizer, LineByLineTextDataset, TransfoXLLMHeadModel, TransfoXLConfig, TransfoXLTokenizer, Trainer, TrainingArguments
import torch
from torch.utils.data import TensorDataset, DataLoader

from tokenizers import Tokenizer, models, pre_tokenizers, decoders
from datasets import load_dataset

print(torch.cuda.is_available())

with open('/home/christopherthompson/Desktop/thesis-contents/jazz_data.txt','r') as f:
    text = f.readlines()

chunk = len(max(text, key=len))

tokenizer = AutoTokenizer.from_pretrained("/home/christopherthompson/Desktop/thesis-contents/vocab_files")
tokenizer.add_special_tokens({'pad_token': '<pad>'})
dataset = LineByLineTextDataset(tokenizer = tokenizer, file_path='/home/christopherthompson/Desktop/thesis-contents/jazz_data.txt',block_size=chunk)

# # Prepare the data and tokenize it
# with open('/home/christopherthompson/Desktop/thesis-contents/jazz_data.txt','r') as f:
#     text = f.read()
#     #text = [lol.replace('\n', '') for lol in text]
#     #text = [lol.split() for lol in text]

# Define the model configuration
config = TransfoXLConfig(output_hidden_states=True, output_past=True)
config.eos_token_id=0
config.pad_token_id=2

# Instantiate the model
model = TransfoXLLMHeadModel(config)

# # Prepare the data and convert it to tensors
# input_ids = torch.tensor(encoded, dtype=torch.long)
# all_mems = encoded.copy()
# for i in range(len(encoded)):
#     all_mems[i] = 10
# mem_len = torch.tensor(all_mems, dtype=torch.long)
# attn_mask = torch.ones(input_ids.shape, dtype=torch.long)
# once_removed = encoded[1:]
# once_removed.append(0)
# target = torch.tensor(once_removed, dtype=torch.long)

# print("INPUT_IDS")
# print(input_ids.shape)
# print("MEM_LEN")
# print(mem_len.shape)
# print("ATTN_MASK")
# print(attn_mask.shape)
# print("TARGET")
# print(target.shape)

# # Create the dataset
# dataset = TensorDataset(input_ids, mem_len, attn_mask, target)

# #dataset = TensorDataset(torch.tensor([[1], [2], [3]]), torch.tensor([[2], [2], [2]]))

from transformers import DataCollatorForLanguageModeling

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm = False, mlm_probability=0.15
)

# Define the TrainingArguments
training_args = TrainingArguments(output_dir='outputs',
                                  eval_steps=100,
                                  per_device_train_batch_size=2,
                                  per_device_eval_batch_size=2,
                                  num_train_epochs=100,
                                  logging_dir='logs',
                                  logging_steps=100000,
                                  save_steps=100000,
                                  learning_rate=5e-5)

# Create the trainer
trainer = Trainer(model=model, tokenizer=tokenizer, args=training_args, data_collator=data_collator, train_dataset=dataset)

# Start training
trainer.train()

# Save model
trainer.save_model('/home/christopherthompson/Desktop/thesis-contents/outputs')