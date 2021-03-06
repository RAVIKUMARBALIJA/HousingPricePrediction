import pandas as pd
import pickle
from utils import loadcolumns,load_predictor,loaddtypes
from preprocessor import load_encoder
import numpy as np

"""
def preprocess_data(record):
    encoder=load_encoder()
    line = np.array(str(record).split(',')).reshape(1,-1)
    record=pd.DataFrame(line,columns=loadcolumns())
    record=record.astype(dtype=loaddtypes(),copy=True)
    record=encoder.transform(record)
    return record
"""
def preprocess_data(record):
    #print(record)
    #print(type(record))
    encoder=load_encoder()
    record=pd.DataFrame(np.array(str(record).split(',')).reshape(1,-1),columns=loadcolumns())
    record=record.astype(dtype=loaddtypes(),copy=True,errors='ignore')
    record=encoder.transform(record)
    return record

def perform_predictions(X):
    X=preprocess_data(X)
    model=load_predictor()
    y=model.predict(X)[0]
    return y

def apply_predict(X):
    y=perform_predictions(X)
    X=X+','+str(y)
    return tuple(X.split(','))