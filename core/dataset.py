import utils
from args import parse_args
import numpy as np
import os

arguments = parse_args()

activates, negatives, backgrounds = utils.load_raw_audio(arguments.data_path)

np.random.seed(arguments.seed)
n_training_sample = 1024

X = []
Y = []

for i in range(n_training_sample):
    x, y = utils.create_training_example(backgrounds[0], activates, negatives, arguments.ty)
    X.append(x.swapaxes(0,1))
    Y.append(y.swapaxes(0,1))

X = np.array(X)
Y = np.array(Y)

if not os.path.exists("XY_train"):
    os.mkdir("XY_train")

np.save("XY_train/X.npy", X)
np.save("XY_train/Y.npy", Y)

X = np.load("/content/XY_train/X.npy")
Y = np.load("/content/XY_train/Y.npy")