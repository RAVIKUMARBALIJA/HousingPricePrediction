#!/usr/bin/python3                                                                                                      
                                                                                                                        
from pyspark import SparkContext                                                                                        
from pyspark.sql import SparkSession                                                                                    
from pyspark.streaming import StreamingContext                                                                         
from pyspark.streaming.kafka import KafkaUtils                                                                          
import pickle
from utils import loadcolumns,load_predictor,loaddtypes
from preprocessor import load_encoder
import numpy as np
import pandas as pd

def handle_rdd(rdd):                                                                                                    
    if not rdd.isEmpty():                                                                                               
        global ss                                                                                                       
        df = ss.createDataFrame(rdd, schema=loadcolumns())                                        
        df.show()                                                                                                       
        df.write.saveAsTable(name='default.housingprice', format='hive', mode='append')

def preprocess_data(record):
    print(record)
    #print(type(record))
    encoder=load_encoder()
    record=pd.DataFrame(np.array(str(record).split(',')).reshape(1,-1),columns=loadcolumns())
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

                                                                                                                                                      
sc = SparkContext(appName="Something")                                                                                   
ssc = StreamingContext(sc, 5)                                                                                           
                                                                                                                        
ss = SparkSession.builder.appName("Something").config("spark.sql.warehouse.dir", "/user/hve/warehouse").config("hive.metastore.uris", "thrift://localhost:9083").enableHiveSupport().getOrCreate()                                                                                                  
                                                                                                                        
ss.sparkContext.setLogLevel('WARN')                                                                                     
                                                                                                                        
ks = KafkaUtils.createDirectStream(ssc, ['housingprice'], {'metadata.broker.list': 'localhost:9092'})                       

#sid = SentimentIntensityAnalyzer()
#added below for custom sentiment analysis

                                                                                                                 
lines = ks.map(lambda x: x[1])

print('*'*10)                                                      
                                                                                                                        
#print(lines)

transform = lines.map(lambda line: apply_predict(line))
#transform = lines.map(lambda line: print(line))


transform.foreachRDD(handle_rdd)                                                                                     
                                                                                                                        
ssc.start()                                                                                                          
ssc.awaitTermination()

# CREATE TABLE tweets (text STRING, words INT, length INT, text STRING) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\\|' STORED AS TEXTFILE;