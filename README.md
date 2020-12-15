# python-accoustic-master

## How To Use
From your command line:

```
# Clone this repository
$ git clone https://github.com/VishnuNarayananSR/python-accoustic-master

# Go into the repository
$ cd python-accoustic-master

# Install dependencies
$ pip install requirements.txt

# Run the app
$ python manage.py runserver
```

## Model Re-training
The model was pretrained on the IRMAS audio dataset. Saved model is in /python-accoustic-master/python_music_master/backend/Trained model/.
Nevertheless, if u wish to retrain the model with your data, place the training data in /python-accoustic-master/python_music_master/backend/rawdata. The folder structure should be maintained.
└── rawdata/
    ├── category1 <br>
    |     └── files <br>
    ├── category 2 <br>
    |      └── files <br>
    └── . . . . . . . <br>
    
Before training preprocess the data by executing ```python preprocess.py``` from a terminal session at the backend folder. The trained data will be saved in processed folder.Then perform training by executing ```python train.py```.
