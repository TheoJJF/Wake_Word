import numpy as np
from pydub import AudioSegment
import random
import sys
import io
import os
import glob
import matplotlib.pyplot as plt
from scipy.io import wavfile

def plot_spectrogram(wav_file):
    rate, data = wavfile.read(wav_file) 
    
    n_fft = 200
    sampling_freq = 8000
    no_overlap = 120
    n_channels = data.ndim  
    
    if n_channels == 1:
      pxx, freqs, bins, im = plt.specgram(data, NFFT=n_fft, Fs=sampling_freq, noverlap=no_overlap)

    elif n_channels == 2:
      pxx, freqs, bins, im = plt.specgram(data[:,0], NFFT=n_fft, Fs=sampling_freq, noverlap=no_overlap)
    
    return pxx

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def load_raw_audio(path):
    '''
    Raw data structure:
        - activates
        - backgrounds
        - negatives
        - samples (Used for testing chime)
    '''
    activates = []
    backgrounds = []
    negatives = []

    for filename in os.listdir(path + "activates"):
        if filename.endswith("wav"):
            activate = AudioSegment.from_wav(path + "activates/" + filename)
            activates.append(activate)

    for filename in os.listdir(path + "backgrounds"):
        if filename.endswith("wav"):
            background = AudioSegment.from_wav(path + "backgrounds/" + filename)
            backgrounds.append(background)

    for filename in os.listdir(path + "negatives"):
        if filename.endswith("wav"):
            negative = AudioSegment.from_wav(path + "negatives/" + filename)
            negatives.append(negative)

    return activates, negatives, backgrounds

def get_random_time_segment(segment_ms):
    """
    Gets a random time segment of duration segment_ms in a 10,000 ms audio clip.

    Arguments:
    segment_ms -- the duration of the audio clip in ms ("ms" stands for "milliseconds")

    Returns:
    segment_time -- a tuple of (segment_start, segment_end) in ms
    """
    segment_start = np.random.randint(low=0, high=10000 - segment_ms)
    segment_end = segment_start + segment_ms - 1

    return segment_start, segment_end

def is_overlapping(segment_time, previous_segments):
    """
    Checks if the time of a segment overlaps with the times of existing segments.

    Arguments:
    segment_time -- a tuple of (segment_start, segment_end) for the new segment
    previous_segments -- a list of tuples of (segment_start, segment_end) for the existing segments

    Returns:
    True if the time segment overlaps with any of the existing segments, False otherwise
    """

    segment_start, segment_end = segment_time

    overlap = False

    for previous_start, previous_end in previous_segments:
        if segment_start <= previous_end and segment_end >= previous_start:
            overlap = True
            break

    return overlap

def insert_audio_clip(background, audio_clip, previous_segments):
    """
    Insert a new audio segment over the background noise at a random time step, ensuring that the
    audio segment does not overlap with existing segments.

    Arguments:
    background -- a 10 second background audio recording.
    audio_clip -- the audio clip to be inserted/overlaid.
    previous_segments -- times where audio segments have already been placed

    Returns:
    new_background -- the updated background audio
    """

    segment_ms = len(audio_clip)
    segment_time = get_random_time_segment(segment_ms)

    retry = 10
    while is_overlapping(segment_time, previous_segments) and retry >= 0:
        segment_time = get_random_time_segment(segment_ms)
        retry -= 1

    if not is_overlapping(segment_time, previous_segments):
        previous_segments.append(segment_time)
        new_background = background.overlay(audio_clip, position = segment_time[0])
    else:
        new_background = background
        segment_time = (10000, 10000)

    return new_background, segment_time

def insert_ones(y, segment_end_ms):
    """
    Update the label vector y. The labels of the 50 output steps strictly after the end of the segment
    should be set to 1. By strictly we mean that the label of segment_end_y should be 0 while, the
    50 following labels should be ones.


    Arguments:
    y -- numpy array of shape (1, Ty), the labels of the training example
    segment_end_ms -- the end time of the segment in ms

    Returns:
    y -- updated labels
    """

    _, Ty = y.shape
    segment_end_y = int(segment_end_ms * Ty / 10000.0)

    if segment_end_y < Ty:
        for i in range(segment_end_y + 1, segment_end_y + 51):
            if i < Ty:
                y[0, i] = 1

    return y

def create_training_example(background, activates, negatives, Ty):
    """
    Creates a training example with a given background, activates, and negatives. 
    Can be used for fine-tuning or making a custom dataset

    Arguments:
    background -- a 10 second background audio recording
    activates -- a list of audio segments of the word "activate"
    negatives -- a list of audio segments of random words that are not "activate"
    Ty -- The number of time steps in the output

    Returns:
    x -- the spectrogram of the training example
    y -- the label at each time step of the spectrogram
    """

    background = background - 10

    y = np.zeros((1, Ty))
    previous_segments = []

    number_of_activates = np.random.randint(0, 5)
    random_indices = np.random.randint(len(activates), size=number_of_activates)
    random_activates = [activates[i] for i in random_indices]

    for random_activate in random_activates:
        background, segment_time = insert_audio_clip(background, random_activate, previous_segments)
        segment_start, segment_end = segment_time

        y = insert_ones(y, segment_end)

    number_of_negatives = np.random.randint(0, 3)
    random_indices = np.random.randint(len(negatives), size=number_of_negatives)
    random_negatives = [negatives[i] for i in random_indices]

    for random_negative in random_negatives:
        background, _ = insert_audio_clip(background, random_negative, previous_segments)

    background = match_target_amplitude(background, -20.0)

    training_file_handle = background.export("train.wav", format="wav")
    training_file = "train.wav"

    x = plot_spectrogram(training_file)
 
    return x, y

def predict_wakeword(file, model):
    audio_clip = AudioSegment.from_wav(file)
    audio_clip = match_target_amplitude(audio_clip, -20.0)
    
    newfile_handle = audio_clip.export("temp.wav", format="wav")
    newfile = "temp.wav"

    x = plot_spectrogram(newfile)
    x = x.swapaxes(0,1)
    x = np.expand_dims(x, axis=0)
    return model.predict(x)

def chime_on_wakeword(file, prediction, threshold):
    audio_clip = AudioSegment.from_wav(file)
    chime_clip = AudioSegment.from_wav("assets/chime.wav")

    Ty = prediction.shape[1]
    consecutive_timesteps = 0
    for i in range(Ty):
        consecutive_timesteps += 1

        if consecutive_timesteps > 20:
            audio_clip = audio_clip.overlay(chime_clip, position = ((i / Ty) * audio_clip.duration_seconds) * 1000)
            consecutive_timesteps = 0

            i = 75 * (i // 75 + 1)
            continue
        
        if prediction[0, i, 0] > threshold:
            i += 1
        else:
            consecutive_timesteps = 0

    audio_clip.export("output.wav", format='wav')