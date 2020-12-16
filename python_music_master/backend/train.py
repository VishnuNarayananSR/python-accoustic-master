from settings import *
from scipy.io import wavfile
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
import kapre

class AudioDataGenerator(tf.keras.utils.Sequence):
    def __init__(self, paths, labels, batch_size, sr, duration, num_classes):
        self.paths = paths
        self.labels = labels
        self.sr = sr
        self.batch_size = batch_size
        self.duration = duration
        self.on_epoch_end()
        self.num_classes = num_classes

    def __len__(self):
        return(len(self.paths)//self.batch_size)
    
    def __getitem__(self, idx):
        cur_batch = self.batch[idx * self.batch_size:(idx + 1) * self.batch_size]
        X = []
        y = []
        for i in cur_batch:
            sr, signal = wavfile.read(self.paths[i])
            X.append(signal)
            lbl = tf.keras.utils.to_categorical(self.labels[i], num_classes=self.num_classes)
            y.append(lbl)
        X = np.array(X)
        y = np.array(y)
        return X, y

    def on_epoch_end(self):
        self.batch = np.arange(len(self.paths))
        np.random.shuffle(self.batch)

def create_model(num_classes, sr=16000, t=1):
    input_shape = (int(sr*t), 1)
    model = tf.keras.models.Sequential([
                                kapre.composed.get_melspectrogram_layer(input_shape=input_shape,
                                                            n_mels=128,
                                                            pad_end=True,
                                                            n_fft=512,
                                                            win_length=400,
                                                            hop_length=160,
                                                            sample_rate=sr,
                                                            return_decibel=True,
                                                            input_data_format='channels_last',
                                                            output_data_format='channels_last'),
                                tf.keras.layers.LayerNormalization(axis=2),
                                tf.keras.layers.TimeDistributed(tf.keras.layers.Conv1D(32, 4, activation='tanh')),
                                tf.keras.layers.ZeroPadding2D(padding=(1,1)), 
                                tf.keras.layers.TimeDistributed(tf.keras.layers.Conv1D(32, 4, activation='relu')),
                                tf.keras.layers.MaxPool2D((3,3)),
                                tf.keras.layers.Dropout(0.1),
                                tf.keras.layers.ZeroPadding2D(padding=(1,1)),
                                tf.keras.layers.TimeDistributed(tf.keras.layers.Conv1D(64, 4, activation='relu')),
                                tf.keras.layers.ZeroPadding2D(padding=(1,1)),
                                tf.keras.layers.TimeDistributed(tf.keras.layers.Conv1D(64, 4, activation='relu')),
                                tf.keras.layers.MaxPool2D((3,3)),
                                tf.keras.layers.Dropout(0.1),
 
                                tf.keras.layers.ZeroPadding2D(padding=(1,1)),
                                tf.keras.layers.TimeDistributed(tf.keras.layers.Conv1D(128, 4, activation='relu')),
                                tf.keras.layers.ZeroPadding2D(padding=(1,1)),
                                tf.keras.layers.TimeDistributed(tf.keras.layers.Conv1D(128, 4, activation='relu')),
                                tf.keras.layers.MaxPool2D((3,3)),
                                tf.keras.layers.Dropout(0.1),
 
                                tf.keras.layers.ZeroPadding2D(padding=(1,1)),
                                tf.keras.layers.TimeDistributed(tf.keras.layers.Conv1D(256, 4, activation='relu')),
                                tf.keras.layers.ZeroPadding2D(padding=(1,1)),
                                tf.keras.layers.TimeDistributed(tf.keras.layers.Conv1D(256, 4, activation='relu')),
                                tf.keras.layers.GlobalMaxPool2D(),
                                tf.keras.layers.Dropout(0.25),
 
                                tf.keras.layers.Flatten(),
                                tf.keras.layers.Dense(1024, activation='relu'),
                                tf.keras.layers.Dropout(0.3),
                                tf.keras.layers.Dense(num_classes, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

def train(path):
    if not os.path.isdir(path):
        print("Dataset path is invalid!", path)
        return 
    categories = sorted(list(map(lambda x:x.name, filter(os.DirEntry.is_dir,os.scandir(path)))))
    np.save(LABELS_FILE, categories, allow_pickle=True)
    y = []
    #labels = sorted(os.listdir(path))
    encoder = LabelEncoder()
    encoder.fit(categories)
    X = []
    y = []
    for lbl in os.scandir(path):
        for f in os.scandir(lbl):
            if f.name.endswith('.wav'):
                X.append(f.path)
                y.append(lbl.name)
    y = encoder.transform(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 6)
    train_gen = AudioDataGenerator(X_train, y_train, BATCH_SIZE, SR, DURATION, len(categories))
    test_gen = AudioDataGenerator(X_test, y_test, BATCH_SIZE, SR, DURATION, len(categories))
    model = create_model(len(categories), SR, t)
    checkpoint = tf.keras.callbacks.ModelCheckpoint(SAVED_MODEL_PATH, monitor='val_loss',
                                                    mode='min', save_best_only=True,
                                                    save_weights_only=False, verbose=1)
    early_stop = tf.keras.callbacks.EarlyStopping(monitor = 'val_accuracy', patience=2)
    model.fit(train_gen, epochs = 30, validation_data=test_gen, callbacks = [checkpoint, early_stop])

if __name__ == '__main__':
    clean_path = BASE_DIR +'/processed'
    train(clean_path)
