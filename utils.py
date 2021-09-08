import numpy as np
import pandas as pd
import os
import sklearn
import sys
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator,TransformerMixin
import pickle





def getMissingDataFeatures(df):
    ser_null_columns = df.isnull().any(axis=0)
    lst_null_columns = [x for x in ser_null_columns.index if ser_null_columns[x]]
    return lst_null_columns

def getNullPercentage(df, feature):
    null_count = len(df[df[feature].isnull()])
    percent_of_nulls = null_count*100/len(df)
    return null_count, percent_of_nulls

def dropFeaturesWithNulls(df, lst_featrues, threshold=75):
    for feature in lst_featrues:
        null_count, percent_of_nulls = getNullPercentage(df, feature)
        #print('Null count in {0} : {1}, Percent of Null: {2}'.format(feature, null_count, percent_of_nulls))
        if(percent_of_nulls > threshold):
         #   print('Droping --- {}'.format(feature))
            df.drop(feature, axis=1, inplace=True)
    return df

def getCatFeatures(df):
    cat_features = df.select_dtypes(include=['object']).columns
    return cat_features

def getCatFeaturesWithNulls(df):
    ser_null_columns = df[getCatFeatures(df)].isnull().any(axis=0)
    lst_null_columns = [x for x in ser_null_columns.index if ser_null_columns[x]]
    return lst_null_columns

def fillNAwithBlank(df, lst_features):
    for feature in lst_features:
        df[feature].fillna('', inplace=True)
    return df

def formulateCondition(lst_features):
    copy_lst_features = lst_features.copy()
    for i, v in enumerate(lst_features):
        if(i == 0):
            copy_lst_features.insert(i*2, 'not ')
        else:    
            copy_lst_features.insert(i*2, ' and not ')
                      
    #print(lst_features)
    return ''.join(copy_lst_features)

def conditionBasedImputation(row, condition, lst_features):
    if condition:
        for feature in lst_features:
            row[feature] = 'NA'
    return row
