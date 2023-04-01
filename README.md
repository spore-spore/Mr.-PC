# Mr. PC
This repository contains the contents of my undergraduate thesis: a machine learning model to generate jazz improvisation. 

By downloading the repository, you should be able to generate your own improvisations using the training script 'new_train' and the vocabulary files in the 'vocab_files' folder (once you have changed the file paths to work in your system).

I cannot include the Filosax data set in its original form, since it utilizes commercial backing tracks. If you would like to get the Filosax data set for yourself, please follow the instructions in the paper to request access. The 'jazz_data' file should be enough to the train model, however. 

What follows is a brief descriptions of each file:
**chord_correction**: specifically for use with the Filosax data set, which had some errors in aligning chord symbols with measures. This script generates new JSON files with the chords in their proper places.

**encoder**: translates a set of JSON files (i.e., those in the Filosax data set) into a string encoding for use in training.

**new_train**: trains a model to generate jazz improvisation.

**music_gen**: uses a model trained with the new_train script to create MIDI files of soloing over a given chord progression.

I also included my processed dataset, which was derived from the Filosax data set:
https://qmro.qmul.ac.uk/xmlui/handle/123456789/75794
