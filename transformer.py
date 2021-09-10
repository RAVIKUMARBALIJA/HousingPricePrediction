from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from transformer_utils import *

                                                                                                                                                      
sc = SparkContext(appName="Something")                                                                                   
ssc = StreamingContext(sc, 5)                                                                                           
                                                                                                                        
ss = SparkSession.builder.appName("Something").config("spark.sql.warehouse.dir", "/user/hve/warehouse").config("hive.metastore.uris", "thrift://localhost:9083").enableHiveSupport().getOrCreate()                                                                                                  
                                                                                                                        
ss.sparkContext.setLogLevel('WARN')                                                                                     
                                                                                                                        
ks = KafkaUtils.createDirectStream(ssc, ['housingprice'], {'metadata.broker.list': 'localhost:9092'})                       



                                                                                                                 
lines = ks.map(lambda x: x[1])

print('*'*10)                                                      
                                                                                                                        
#print(lines)

transform = lines.map(lambda line: apply_predict(line))



transform.foreachRDD(handle_rdd)                                                                                     
                                                                                                                        
ssc.start()                                                                                                          
ssc.awaitTermination()

# CREATE TABLE tweets (text STRING, words INT, length INT, text STRING) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\\|' STORED AS TEXTFILE;