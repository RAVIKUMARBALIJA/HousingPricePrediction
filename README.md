# HousingPricePreditction
Housingpriceprediction

## Please find below instructions on how to test

## Used :
 python : 3.6.9
 pyspark : 2.4.6
 

## Without Docker
### Flask - pyspark - kafka  - Ui integration - successfull
### 1. run below commands to bring kafka zookeeper services, kafka topic and then run the spark-submit job to bring the application up./
       
       i. ~$ cd kafka/
       ~/kafka$ bin/zookeeper-server-start.sh config/zookeeper.properties
       ii.  ~$ cd kafka/
       ~/kafka$ bin/kafka-server-start.sh config/server.properties
        
    iii. ~/kafka$ bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1      --topic housingprice
    
    iv. source hackathon2/bin/activate
    
        cd HousingPricePrediction
        
        spark-submit --jars home/ravikumar/spark-streaming-kafka-0-8-assembly_2.11-2.4.3.jar wsgi.py
        
        Result : UI has been brought up. you may supply required values and click on predict.
        You will be able to see the predcited SalePrice.

### 2. fake streaming the dataset using kafka - predict the Sale price and show it on the UI.
### file data set -pyspark - kafka - prediction - show it on the console
### run below commands to bring kafka zookeeper services, kafka topic and then run the spark-submit job to start fake streaming and prediction.
    i. ~$ cd kafka/
      ~/kafka$ bin/zookeeper-server-start.sh config/zookeeper.properties
      ii.  ~$ cd kafka/
        ~/kafka$ bin/kafka-server-start.sh config/server.properties
    iii. ~/kafka$ bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1      --topic housingprice
    iv. source hackathon2/bin/activate
        cd HousingPricePrediction
        python3 fake_stream.py 
    iv. source hackathon2/bin/activate
        cd HousingPricePrediction
        spark-submit --jars home/ravikumar/spark-streaming-kafka-0-8-assembly_2.11-2.4.3.jar transformer.py
        Result : you would be able to see the fake stream as well the live prediction of the SalePrice.

### 3. fake streaming the dataset using kafka - predict the Sale price and send it to hive data store.
### file data set -pyspark - kafka - prediction - hive
### run below commands to bring kafka zookeeper services, kafka topic and then run the spark-submit job to start fake streaming and prediction.
    prerequisites: setup hadoop  hive and bring up the hadoop name node, data node and secondary data node. would be ok if you bring the all of them in the same server for practice.
    i. hive --service metastore
    ii. ~$ cd kafka/
      ~/kafka$ bin/zookeeper-server-start.sh config/zookeeper.properties
      iii.  ~$ cd kafka/
        ~/kafka$ bin/kafka-server-start.sh config/server.properties
    iv. ~/kafka$ bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1      --topic housingprice
    v. source hackathon2/bin/activate
        cd HousingPricePrediction
        python3 fake_stream.py 
    vi. source hackathon2/bin/activate
        cd HousingPricePrediction
        spark-submit --jars home/ravikumar/spark-streaming-kafka-0-8-assembly_2.11-2.4.3.jar transformer_hive.py
    vii. open hive shell using hive command
        run select * from housingprice. or run see_contents.py
        result : You would be able to see the streamed records.

### 4. Docker- compose solution for the 2nd solution above.
   setup is almost completed. servicecs are coming up. but However solution is trying to bring zookeeper and kafka services twice on the same port due to which docker-compose build is not successfull.
   commands: 
   i. cd hackathon
   
   ii. source hackathon2/bin/activate
   
   iii. cd HousingPricePrediction
   
   iv. sudo docker-compose up --build
   
 
   result : 80% completed.
   
   Please refer to HousingPricePrediction/application_screens.docx for screenshots of the applications.
   


# descriptions

#### preprocessor.py - contains code for cleanup and encoding techniques.
#### fake_stream.py  - to fake stream data from both train_set and test_set. this module randomly picks up either train_set or test set and do streming through kafka.
#### EDA, EDA2  - Exploratory analysis done for the problem.
#### model_selection.ipynb - contains code for model selection - selected Decision tree regressor.
#### predictons_test.ipynb - done the predictions for test set.
#### table_creation.txt - script to create table in hive
#### transformer.py - kafka consumer to predict the saleprice and show it on console.
#### transfromer_hive.py - kafka consumer to predict the saleprice and send it to hive.
#### wsgi.py - code contains to bring the flask application Ui.

