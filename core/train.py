import model
from args import parse_args
import tensorflow.keras.models

arguments = parse_args()
wake_word = model.model1(input_shape=(arguments.tx, arguments.n_freqs))

X = arguments.X_dataset
Y = arguments.Y_dataset

# If there is pre-trained weights, could use script
if arguments.pretrained:
    wake_word.load_weights(arguments.pretrained_path)

optimizer = model.Adam(learning_rate=1e-6)
metrics = [model.Precision(), model.Recall()]
wake_word.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=metrics)

wake_word.fit(X, Y, batch_size=arguments.batch_size, epochs=arguments.epoch)