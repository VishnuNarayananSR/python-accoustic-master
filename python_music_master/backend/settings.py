import os

SR = 16000  #sample rate
t = 1  #length of each audio file in seconds
DURATION = t * SR #duration of audio signal
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #project path
BATCH_SIZE = 32 #Training batch size
SAVED_MODEL_PATH = BASE_DIR + '/Trained model/Conv1D' #path to save trained model
MEDIA_DIR = os.path.abspath(__file__ + 2 *'/..') + '/media'    #path to media folder
PREDICTION_THRESHOLD=0.5    #How confident the model should be, to print a label as valid output
LABELS_FILE = BASE_DIR+'/labelfile'
