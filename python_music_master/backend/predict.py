import sys
import os
sys.path.append(os.path.dirname(__file__))
from settings import *
from preprocess import purifier
from scipy.io import wavfile
from librosa import to_mono, resample
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import tensorflow as tf
from patoolib import extract_archive
class ffmpegError(Exception):
    pass
class unsupportedFile(Exception):
    pass
class zipError(Exception):
    pass
def convert_to_wav(file_name):
    file_path = f'{MEDIA_DIR}/{file_name}'
    try:
        if file_name.lower().endswith('.mp3'):
            try:
                if sys.platform.lower() != 'linux':
                    if not os.path.isdir(f'{BASE_DIR}/ffmpeg-2020-12-20-git-ab6a56773f-full_build'):
                        try:
                            extract_archive(f'{BASE_DIR}/ffmpeg-2020-12-20-git-ab6a56773f-full_build.7z', outdir=BASE_DIR)
                        except:
                            raise zipError
                    os.environ["PATH"] += (os.pathsep + BASE_DIR + r'\ffmpeg-2020-12-20-git-ab6a56773f-full_build\bin')
                file_name = file_name.split('.')[0] + '.wav'
                AudioSegment.from_mp3(file_path).export(f'{MEDIA_DIR}/{file_name}', format="wav")
                os.remove(file_path)
                return file_name
            except zipError:
                raise zipError
            except Exception as e:
                print('\n<<<<<<<<<<<<<<<<<<<<<<<<<<<Exception>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print(e)
                raise ffmpegError
        else:
            file_name = file_name.split('.')[0] + '.wav'
            data, samplerate = sf.read(file_path)
            sf.write(f'{MEDIA_DIR}/{file_name}', data, samplerate)
            os.remove(file_path)
            return file_name
    except zipError:
        raise zipError
    except ffmpegError:
        raise ffmpegError
    except Exception as e:
        print('\n<<<<<<<<<<<<<<<<<<<<<<<<<<<Exception>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(e)
        raise unsupportedFile


def predict(file_name):
    try:
        if not file_name.lower().endswith('.wav'):
            file_name = convert_to_wav(file_name)
        file_path = f'{MEDIA_DIR}/{file_name}'
        sr, signal = wavfile.read(file_path)
    except ffmpegError:
        return ["Sorry. Your system is incompatible with the ffmpeg version. Please try inputting other file types than mp3"]
    except unsupportedFile:
        return ["Unsupported File Recieved!"]
    except zipError:
        return ["You must have 7zip installed to extract dependencies. This is required only for the first run"]
    model = tf.keras.models.load_model(SAVED_MODEL_PATH)
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
