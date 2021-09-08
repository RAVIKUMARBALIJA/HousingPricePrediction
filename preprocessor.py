import numpy as np
import pandas as pd
import os
import sklearn
import sys
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator,TransformerMixin
from utils import getMissingDataFeatures,getNullPercentage,dropFeaturesWithNulls,getCatFeatures,getCatFeaturesWithNulls,fillNAwithBlank
from utils import formulateCondition,conditionBasedImputation

class FillNAandCleanUp(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X.fillna(value=X.mean()[['LotFrontage']], inplace=True)
        X.fillna(value=X.mean()[['GarageArea']], inplace=True)
        X.fillna(value=X.median()[['BsmtFinSF1']], inplace=True)
        X['MasVnrArea'].fillna(value=0, inplace=True)
        X['GarageCars'].fillna(value=2, inplace=True)
        X['BsmtHalfBath'].fillna(value=0, inplace=True)
        X['BsmtFullBath'].fillna(value=0, inplace=True)
        
        
        #interpolation, we have to reindex the dataframe. Then interpolate, then drop(reset) the index.
        X.index = X['YearBuilt']
        X['GarageYrBlt'] = X['GarageYrBlt'].interpolate()
        X.reset_index(drop=True, inplace=True)

        X.rename(columns={'1stFlrSF':'FstFlrSF', '2ndFlrSF':'SecndFlrSF', '3SsnPorch':'ThreeSsnPorch'}, \
                                                                                                     inplace=True)
        X.BsmtCond.fillna('TA', inplace=True)

        # Droping inconsistent data from the data frame.
        X.drop(X[X['GarageYrBlt'] < X['YearBuilt']].index, inplace=True)

        X.drop('MasVnrArea', axis=1, inplace=True)
        X.drop('MasVnrType', axis=1, inplace=True)
        X = dropFeaturesWithNulls(X, getCatFeaturesWithNulls(X))
        
        lst_featurs = ['BsmtQual', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', \
                       'GarageType', 'GarageFinish', 'GarageQual', 'GarageCond']
        X = fillNAwithBlank(X, lst_featurs)
        
        lst_features_bsmt = ['BsmtQual', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2']
        condition_bsmt = formulateCondition(lst_features_bsmt)
        X = X.apply(lambda row: conditionBasedImputation(row, condition_bsmt, lst_features_bsmt), axis=1)
        
        lst_features_garag = ['GarageType', 'GarageFinish', 'GarageQual', 'GarageCond']
        condition_garag = formulateCondition(lst_features_garag)
        X = X.apply(lambda row: conditionBasedImputation(row, condition_garag, lst_features_garag), axis=1)

        X.drop(X[X.Electrical.isnull()].index, inplace=True)
        X.drop('FireplaceQu', axis = 1, inplace = True)
        X.dropna(how='any',axis=0,inplace=True)
        return X


class CatFeatureCleanUpAndEncode(BaseEstimator, TransformerMixin):
     
    
    def __init__(self, lst_categories, feature, replace_val = None, lblEncode= True):
        self.lst_categories = lst_categories
        self.feature = feature
        if replace_val:
            self.replace_val = replace_val
        else:
            self.replace_val = 'OO_TH_ER'
            
        
        self.lblEncode = lblEncode
        

    #X is trainset dataframe
    def fit(self, X, y=None):
        return self
   
    def transform(self, X, y=None):
        
        #get all the unique values which are in a "catergorical" feature, but are actually not part of data dictionary
        #eg: for MSZoning column, C(all) is the available in data, but it is not part of data dictionary
        #actually it should be representated as "C", because of data entry issue, in data it is representated as C(all)
        ser_non_cat_values = X[~ X[self.feature].isin(self.lst_categories)][self.feature]
        
        #if you have any such values which are part of data, and not part of data dictionary, correct them with 
        #proper value. For eg: here we are replacinng MSZoning's C(all) with C
        
        if(ser_non_cat_values.shape[0] > 0):
            X.loc[X[~ X[self.feature].isin(self.lst_categories)].index, self.feature] = self.replace_val
        
        # Convert to categorical feature
        X[self.feature] = pd.Categorical(X[self.feature], categories=self.lst_categories)
        
        if self.lblEncode:
            # Do label encoding
            X[self.feature] = X[self.feature].cat.codes
        else:
            # Do One-Hot encoding
            X = pd.get_dummies(X, columns=[self.feature], prefix=[self.feature], drop_first=True)
        return X
lst_MSZoning_cat = ['A','C','FV','I','RH','RL','RP','RM']
lst_Street_cat = ['Grvl','Pave']
lst_LotShape_cat = ['Reg','IR1','IR2','IR3']
lst_LandContour_cat = ['Lvl','Bnk','HLS','Low']
lst_Utilities_cat = ['AllPub','NoSewr','NoSeWa','ELO']
lst_LandSlope_cat = ['Gtl','Mod','Sev']
lst_Condition1_cat = ['Artery','Feedr','Norm','RRNn','RRAn','PosN','PosA','RRNe','RRAe']
lst_Condition2_cat = ['Artery','Feedr','Norm','RRNn','RRAn','PosN','PosA','RRNe','RRAe']
lst_BldgType_cat = ['1Fam','2FmCon','Duplx','TwnhsE','TwnhsI']
lst_HouseStyle_cat = ['1Story','1.5Fin','1.5Unf','2Story','2.5Fin','2.5Unf','SFoyer','SLvl']
lst_RoofStyle_cat = ['Flat','Gable','Gambrel','Hip','Mansard','Shed']
lst_RoofMatl_cat = ['ClyTile','CompShg','Membran','Metal','Roll','Tar&Grv','WdShake','WdShngl']
lst_Exterior1st_cat = ['AsbShng','AsphShn','BrkComm','BrkFace','CBlock','CemntBd','HdBoard',\
                       'ImStucc','MetalSd','Other','Plywood', 'PreCast','Stone','Stucco',\
                       'VinylSd','Wd Sdng','WdShing']
lst_Exterior2nd_cat = ['AsbShng','AsphShn','BrkComm','BrkFace','CBlock','CemntBd','HdBoard',\
                       'ImStucc','MetalSd','Other','Plywood','PreCast','Stone','Stucco',\
                       'VinylSd','Wd Sdng','WdShing']
lst_ExterQual_cat = ['Ex','Gd','TA','Fa','Po']
lst_ExterCond_cat = ['Ex','Gd','TA','Fa','Po']
lst_Foundation_cat = ['BrkTil','CBlock','PConc','Slab','Stone','Wood']
lst_BsmtQual_cat = ['Ex','Gd','TA','Fa','Po','NA']
lst_BsmtCond_cat = ['Ex','Gd','TA','Fa','Po','NA']
lst_BsmtExposure_cat = ['Gd','Av','Mn','No','NA'] 
lst_BsmtFinType1_cat = ['GLQ','ALQ','BLQ','Rec','LwQ','Unf','NA']
lst_BsmtFinType2_cat = ['GLQ','ALQ','BLQ','Rec','LwQ','Unf','NA']
lst_Heating_cat = ['Floor','GasA','GasW','Grav','OthW','Wall']
lst_HeatingQC_cat = ['Ex','Gd','TA','Fa','Po']
lst_CentralAir_cat = ['N','Y']
lst_Electrical_cat = ['SBrkr','FuseA','FuseF','FuseP','Mix']
lst_KitchenQual_cat = ['SBrkr','FuseA','FuseF','FuseP','Mix']
lst_KitchenQual_cat = ['Ex','Gd','TA','Fa','Po']
lst_Functional_cat = ['Typ','Min1','Min2','Mod','Maj1','Maj2','Sev','Sal']
lst_GarageType_cat = ['2Types','Attchd','Basment','BuiltIn','CarPort','Detchd','NA']
lst_GarageFinish_cat = ['Fin','RFn','Unf','NA']
lst_GarageQual_cat = ['Ex','Gd','TA','Fa','Po','NA']
lst_GarageCond_cat = ['Ex','Gd','TA','Fa','Po','NA']
lst_PavedDrive_cat = ['Y','P','N']
lst_SaleType_cat = ['WD ','CWD','VWD','New','COD','Con','ConLw','ConLI','ConLD','Oth']
lst_SaleCondition_cat = ['Normal','Abnorml','AdjLand','Alloca','Family','Partial']                      
lst_LotConfig_cat = ['Inside','Corner','CulDSac','FR2','FR3']
lst_Neighborhood_cat = ['Blmngtn','Blueste','BrDale','BrkSide','ClearCr','CollgCr','Crawfor',\
                        'Edwards','Gilbert','IDOTRR','MeadowV','Mitchel','Names','NoRidge',\
                        'NPkVill','NridgHt','NWAmes','OldTown','SWISU','Sawyer','SawyerW',\
                        'Somerst','StoneBr','Timber','Veenker']

def load_feature_cleaner():
    return Pipeline([('fillNAandCleanUp', FillNAandCleanUp())])

def load_encoder():
    cat_feature_encod_pipeline = Pipeline([
        ('lst_MSZoning_cat', CatFeatureCleanUpAndEncode(lst_MSZoning_cat, 'MSZoning', 'C')),
        ('lst_Street_cat', CatFeatureCleanUpAndEncode(lst_Street_cat, 'Street')),
        ('lst_LotShape_cat', CatFeatureCleanUpAndEncode(lst_LotShape_cat, 'LotShape')),
        ('lst_LandContour_cat', CatFeatureCleanUpAndEncode(lst_LandContour_cat, 'LandContour')),
        ('lst_Utilities_cat', CatFeatureCleanUpAndEncode(lst_Utilities_cat, 'Utilities')),
        ('lst_LandSlope_cat', CatFeatureCleanUpAndEncode(lst_LandSlope_cat, 'LandSlope')),
        ('lst_Condition1_cat', CatFeatureCleanUpAndEncode(lst_Condition1_cat, 'Condition1')),    
        ('lst_Condition2_cat', CatFeatureCleanUpAndEncode(lst_Condition2_cat, 'Condition2')),
        ('lst_BldgType_cat', CatFeatureCleanUpAndEncode(lst_BldgType_cat, 'BldgType')),    
        ('lst_HouseStyle_cat', CatFeatureCleanUpAndEncode(lst_HouseStyle_cat, 'HouseStyle')),
        ('lst_RoofStyle_cat', CatFeatureCleanUpAndEncode(lst_RoofStyle_cat, 'RoofStyle')),
        ('lst_RoofMatl_cat', CatFeatureCleanUpAndEncode(lst_RoofMatl_cat, 'RoofMatl')),
        ('lst_Exterior1st_cat', CatFeatureCleanUpAndEncode(lst_Exterior1st_cat, 'Exterior1st')),    
        ('lst_Exterior2nd_cat', CatFeatureCleanUpAndEncode(lst_Exterior2nd_cat, 'Exterior2nd')),
        ('lst_ExterQual_cat', CatFeatureCleanUpAndEncode(lst_ExterQual_cat, 'ExterQual')), 
        ('lst_ExterCond_cat', CatFeatureCleanUpAndEncode(lst_ExterCond_cat, 'ExterCond')),
        ('lst_Foundation_cat', CatFeatureCleanUpAndEncode(lst_Foundation_cat, 'Foundation')),
        ('lst_BsmtQual_cat', CatFeatureCleanUpAndEncode(lst_BsmtQual_cat, 'BsmtQual')),
        ('lst_BsmtCond_cat', CatFeatureCleanUpAndEncode(lst_BsmtCond_cat, 'BsmtCond')),    
        ('lst_BsmtExposure_cat', CatFeatureCleanUpAndEncode(lst_BsmtExposure_cat, 'BsmtExposure')),
        ('lst_BsmtFinType1_cat', CatFeatureCleanUpAndEncode(lst_BsmtFinType1_cat, 'BsmtFinType1')), 
        ('lst_BsmtFinType2_cat', CatFeatureCleanUpAndEncode(lst_BsmtFinType2_cat, 'BsmtFinType2')),
        ('lst_Heating_cat', CatFeatureCleanUpAndEncode(lst_Heating_cat, 'Heating')),
        ('lst_HeatingQC_cat', CatFeatureCleanUpAndEncode(lst_HeatingQC_cat, 'HeatingQC')),
        ('lst_CentralAir_cat', CatFeatureCleanUpAndEncode(lst_CentralAir_cat, 'CentralAir')),
        ('lst_Electrical_cat', CatFeatureCleanUpAndEncode(lst_Electrical_cat, 'Electrical')),    
        ('lst_KitchenQual_cat', CatFeatureCleanUpAndEncode(lst_KitchenQual_cat, 'KitchenQual')),
        ('lst_Functional_cat', CatFeatureCleanUpAndEncode(lst_Functional_cat, 'Functional')), 
        ('lst_GarageType_cat', CatFeatureCleanUpAndEncode(lst_GarageType_cat, 'GarageType')),
        ('lst_GarageFinish_cat', CatFeatureCleanUpAndEncode(lst_GarageFinish_cat, 'GarageFinish')),
        ('lst_GarageQual_cat', CatFeatureCleanUpAndEncode(lst_GarageQual_cat, 'GarageQual')),
        ('lst_GarageCond_cat', CatFeatureCleanUpAndEncode(lst_GarageCond_cat, 'GarageCond')),    
        ('lst_PavedDrive_cat', CatFeatureCleanUpAndEncode(lst_PavedDrive_cat, 'PavedDrive')),
        ('lst_SaleType_cat', CatFeatureCleanUpAndEncode(lst_SaleType_cat, 'SaleType')), 
        ('lst_SaleCondition_cat', CatFeatureCleanUpAndEncode(lst_SaleCondition_cat, 'SaleCondition')),
    
        ('lst_LotConfig_cat', CatFeatureCleanUpAndEncode(lst_LotConfig_cat, 'LotConfig', \
                                                         lblEncode= False)),
        ('lst_Neighborhood_cat', CatFeatureCleanUpAndEncode(lst_Neighborhood_cat, 'Neighborhood', \
                                                            lblEncode=False))
      ])
    return cat_feature_encod_pipeline

def load_predictor():
    return pickle.load(open('models/predictor.pkl','rb'))