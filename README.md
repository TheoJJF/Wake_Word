# Wake Word

This repository contains a wake word detection model along with a pre-trained weights file. Given raw audio data, a chime will sound after the word "activate".

## Model1's Architecture:

1. Conv1D layer
1. BatchNormalization layer
1. Activation layer
1. Dropout layer
1. GRU layer
1. Dropout layer
1. BatchNormalization layer
1. GRU layer
1. Dropout layer
1. BatchNormalization layer
1. Dropout layer
1. TimeDistributed Dense layer

## Model2's Architecture: (WORK IN PROGRESS)

1. Conv1D layer
1. LayerNormalization layer
1. Bidirectional LSTM layer with Dropout
1. Bidirectional LSTM layer with Dropout
1. Dense layer

## 🚀 Getting Started

### Cloning the repository

```
git clone https://github.com/TheoJJF/Wake_Word.git
cd Wake_Word
```

### Setting up environment [Optional] 

```
conda create -n myEnvironment
conda activate myEnvironment
```

### Installing dependencies

```
pip3 install -r requirements.txt
```

### Note
For training please refer to `core/train.py`, and for testing please refer to `notebook/wake_word_notebook.ipynb`

## 🛠️ Script Arguments
There are a few places for potential adjustments. Below contains a list of possible arguments. 

- `--tx`
    - REQUIRED
    - The number of time step input to the model from the spectrogram.

- `--ty`
    - REQUIRED
    - The number of time steps in the output of the model.

- `--n_freqs`
    - REQUIRED
    - The number of frequenices input to the model at each time step of the spectrogram.

- `--seed`
    - REQUIRED
    - The set seed for random

- `--n_training_samples`
    - REQUIRED
    - The number of training examples that you wish to create for your dataset.

- `--data_path`
    - REQUIRED
    - Path to raw audio data.

- `--pretrained`
    - OPTIONAL
    - Determines whether to load pre-trained weights.

- `--pretrained_path`
    - OPTIONAL
    - Path to pre-trained weights.

- `--batch_size`
    - OPTIONAL

- `--epoch`
    - OPTIONAL

- `--X_dataset`
    - REQUIRED
    - Path to spectrograms.

- `--Y_dataset`
    - REQUIRED
    - Path to labels.

## 🗒️ TO-DO List

1. Finish creating custom dataset for Model2
1. Train and fine-tune Model2
1. Create a real-time audio pipeline for predictions
