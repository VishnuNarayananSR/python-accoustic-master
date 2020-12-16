import sys
import os
sys.path.append(os.path.dirname(__file__))
from settings import *
from preprocess import purifier
from scipy.io import wavfile
from librosa import to_mono, resample
import numpy as np
import tensorflow as tf


def predict(file_name):
    model = tf.keras.models.load_model(SAVED_MODEL_PATH)
    if not file_name.lower().endswith('.wav'):
        return ['Only wav files are supported. Due to compression in other audio formats, model will not perform well']
    file_path = f'{MEDIA_DIR}/{file_name}'
    try:
        sr, signal = wavfile.read(file_path)
    except:
        return ["Unsupported File Recieved!"]
    signal = signal.astype(np.float32).T
    if signal.shape[0] == 2:
        signal = to_mono(signal)
    elif signal.shape[0] == 1:
        signal = to_mono(signal.reshape(-1))
    signal = resample(signal, sr, SR)
    sr = SR
    signal = signal.astype(np.int16)
    mask = purifier(signal, sr, 100)
    signal = signal[mask]
    X_test = []
    for i in range(0, signal.shape[0], DURATION):
        signal_strip = signal[i:i+DURATION]
        signal_strip = signal_strip.reshape(-1,1)
        if signal_strip.shape[0] < DURATION:
            tmp = np.zeros((DURATION,1))
            tmp[:signal_strip.shape[0],:] = signal_strip
            signal_strip = tmp
        X_test.append(signal_strip)
    X_test = np.array(X_test)
    dense_pred = model.predict(X_test)
    simplified_pred = np.mean(dense_pred, axis=0)
    labels = np.load(LABELS_FILE, allow_pickle=True)
    bool_mask = simplified_pred > PREDICTION_THRESHOLD
    result = []
    for i, j in enumerate(labels):
        if bool_mask[i]:
            result.append(j)
    if not result:
        return ["Oops Sorry.I couldn't distinguish any sounds...I realise I'm a noob."]
    return result

# def predicttest(file_name):
#     return ['Place holder result','Placeholder again']
