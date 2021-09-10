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
        df = ss.createDataFrame(rdd, schema=loadcolumns(True))                                        
        df.show()                                                                       
        #commenting hive table insert                                
        #df.write.saveAsTable(name='default.housingprice', format='hive', mode='append')

def preprocess_data(record):
    #print(record)
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
    #print(X)
    X=X+','+str(y)
    #print(f'Predicted SalePrice : {y}')
    return tuple(X.split(','))

BROKER = 'localhost:9092'                                                                                               
TOPIC = 'housingprice'
filename= random.choice(('for_stream_test.csv','for_stream_train.csv'))
path='data/'+str(filename)                                                                                                   
                                                                                                                        
TEST_FILE = os.path.abspath(path)                                                                                    
RECORDS = open(TEST_FILE).read().splitlines()                                                                             
                                                                                                                            
try:                                                                                                                    
    p = KafkaProducer(bootstrap_servers=BROKER)                                                                         
except Exception as e:                                                                                                  
    print(f"ERROR --> {e}")                                                                                             
    sys.exit(1)                                                                                                        
                                                                                                                            
    

                                                                                                                                                      
sc = SparkContext(appName="Something")                                                                                   
ssc = StreamingContext(sc, 5)                                                                                           
                                                                                                                        
ss = SparkSession.builder.appName("Something").config("spark.sql.warehouse.dir", "/user/hve/warehouse").config("hive.metastore.uris", "thrift://localhost:9083").enableHiveSupport().getOrCreate()                                                                                                  
                                                                                                                        
ss.sparkContext.setLogLevel('WARN')                                                                                     
                                                                                                                        
ks = KafkaUtils.createDirectStream(ssc, ['housingprice'], {'metadata.broker.list': 'localhost:9092'})                       

while True:                                                                                                             
        message= RECORDS[randint(0, len(RECORDS)-1)]                                                               
        print(f">>> '{message}'")                                                                                           
        p.send(TOPIC, bytes(message, encoding="utf8"))                                                                      
        #sleep(randint(1,4))


                                                                                                                 
        lines = ks.map(lambda x: x[1])

        print('*'*10)                                                      
                                                                                                                                
        #print(lines)

        transform = lines.map(lambda line: apply_predict(line))



        transform.foreachRDD(handle_rdd)                                                                                     
                                                                                                                        
ssc.start()                                                                                                          
ssc.awaitTermination()

# CREATE TABLE tweets (text STRING, words INT, length INT, text STRING) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\\|' STORED AS TEXTFILE;