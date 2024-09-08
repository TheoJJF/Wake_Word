import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        "Training/Dataset Arguments"
    )

    parser.add_argument(
        "--tx",
        required=True,
        type=int,
        help="The number of time step input to the model from the spectrogram"
    )

    parser.add_argument(
        "--ty",
        required=True,
        type=int,
        help="The number of time steps in the output of the model"
    )

    parser.add_argument(
        "--n_freqs",
        required=True,
        type=int,
        help="The number of frequencies input to the model at each time step of the spectrogram"
    )

    parser.add_argument(
        "--seed",
        required=True,
        type=int,
        help="Set seed for numpy random"
    )

    parser.add_argument(
        "--n_training_samples",
        required=True,
        type=int,
        help="Set number of training examples that want to be created for your dataset"
    )

    parser.add_argument(
        "--data_path",
        required=True,
        type=str,
        help="Path to your raw audio data"
    )

    parser.add_argument(
        "--pretrained",
        required=True,
        type=bool,
        help="Used for training script to determine if you would like to load pre-trained weights"
    )

    parser.add_argument(
        "--pretrained_path",
        required=True,
        type=str,
        help="Pre-trained weights path"
    )

    parser.add_argument(
        "--batch_size",
        required=True,
        type=int
    )

    parser.add_argument(
        "--epoch",
        required=True,
        type=int
    )

    parser.add_argument(
        "--X_dataset",
        required=True,
        type=str,
        help="Path to spectrograms"
    )

    parser.add_argument(
        "--Y_dataset",
        required=True,
        type=str,
        help="Path to labels"
    )