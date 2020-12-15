from settings import *
import argparse
from glob import glob
from tqdm import tqdm
from scipy.io import wavfile
from librosa import to_mono, resample
import numpy as np
import pandas as pd


def purifier(y, rate, threshold):
    mask = []
    y = pd.Series(y).apply(np.abs)
    local_maximas = y.rolling(window=int(rate/20),
                       min_periods=1,
                       center=True).max()
    for lm in local_maximas:
        if lm > threshold:
            mask.append(True)
        else:
            mask.append(False)
    return mask

def save_file(strip, sr, clean_path, cls_name, file_name, idx):
    file_name = file_name.replace('.wav', '')
    target_dir = os.path.join(clean_path, cls_name)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    save_path = os.path.join(target_dir,f'{file_name}_{idx}.wav')
    if os.path.exists(f'{save_path}'):
        return
    wavfile.write(save_path, sr, strip)

def preprocess(raw_path, clean_path):
    raw_path = os.path.join(BASE_DIR, raw_path)
    clean_path = os.path.join(BASE_DIR, clean_path)
    if not os.path.isdir(raw_path):
        print('Path to Raw dataset is invalid!')
        return
    if not os.path.isdir(clean_path):
        os.mkdir(clean_path)
    for cls in os.scandir(raw_path):
        if cls.is_dir:
            for item in tqdm(os.scandir(cls), total=len(os.listdir(cls))):
                if item.name.endswith('.wav'):
                    audio = item.path
                    sr, signal = wavfile.read(audio)
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
                    if signal.shape[0] < DURATION:      #if the audio after purification is less than 2s, append zeros
                        rectified_signal = np.zeros((DURATION,), dtype= np.int16)
                        rectified_signal[:signal.shape[0]] = signal
                        save_file(signal, sr, cls.name, item.name, 0)
                    else:
                        trunc = signal.shape[0] % DURATION
                        for i, j in enumerate(range(0,signal.shape[0]-trunc, DURATION)):
                            strip = signal[j : j + DURATION]
                            save_file(strip, sr, clean_path, cls.name, item.name, i)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=str ,default='rawdata')
    args, _ = parser.parse_known_args()
    raw_path = args.src
    clean_path = 'processed'
    preprocess(raw_path, clean_path)
