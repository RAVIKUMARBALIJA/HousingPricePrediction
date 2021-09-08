#!/usr/bin/python3                                                                                                      
                                                                                                                        
from pyspark import SparkContext                                                                                        
from pyspark.sql import SparkSession                                                                                    
from pyspark.streaming import StreamingContext                                                                         
from pyspark.streaming.kafka import KafkaUtils                                                                          
import pickle
from utils import loadcolumns,load_predictor

def handle_rdd(rdd):                                                                                                    
    if not rdd.isEmpty():                                                                                               
        global ss                                                                                                       
        df = ss.createDataFrame(rdd, schema=loadcolumns())                                        
        df.show()                                                                                                       
        df.write.saveAsTable(name='default.housingprice', format='hive', mode='append')

def perform_predictions(X):
    model= load_predictor()
    

                                                                                                                                                           
sc = SparkContext(appName="Something")                                                                                   
ssc = StreamingContext(sc, 5)                                                                                           
                                                                                                                        
ss = SparkSession.builder.appName("Something").config("spark.sql.warehouse.dir", "/user/hve/warehouse").config("hive.metastore.uris", "thrift://localhost:9083").enableHiveSupport().getOrCreate()                                                                                                  
                                                                                                                        
ss.sparkContext.setLogLevel('WARN')                                                                                     
                                                                                                                        
ks = KafkaUtils.createDirectStream(ssc, ['housingprice'], {'metadata.broker.list': 'localhost:9092'})                       

#sid = SentimentIntensityAnalyzer()
#added below for custom sentiment analysis

                                                                                                                 
lines = ks.map(lambda x: x[1])

print('*'*10)                                                      
                                                                                                                        
#transform = lines.map(lambda tweet: (tweet, int(len(tweet.split())), int(len(tweet)), sid.polarity_scores(tweet)))
print(lines)
transform = lines.map(lambda tweet: (tweet, int(len(tweet.split())), int(len(tweet)), str(sid.predict_proba(tfidf.transform([clean_text(tweet)]))[0])))


#transform = lines.map(lambda line : ())

transform.foreachRDD(handle_rdd)                                                                                     
                                                                                                                        
ssc.start()                                                                                                          
ssc.awaitTermination()

# CREATE TABLE tweets (text STRING, words INT, length INT, text STRING) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\\|' STORED AS TEXTFILE;