import pandas as pd
import pickle
from utils import loadcolumns,load_predictor,loaddtypes
from preprocessor import load_encoder
import numpy as np


def handle_rdd(rdd):                                                                                                    
    if not rdd.isEmpty():                                                                                               
        global ss                                                                                                       
        df = ss.createDataFrame(rdd, schema=loadcolumns())                                        
        df.show()                                                                                                       
        df.write.saveAsTable(name='default.housingprice', format='hive', mode='append')

def preprocess_data(record):
    encoder=load_encoder()
    record=pd.DataFrame(np.array(record.split(',')).reshape(1,-1),columns=loadcolumns())
    record=record.astype(dtype=loaddtypes(),copy=True)
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