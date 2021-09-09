#!/usr/bin/python3                                                                                                      
                                                                                                                        
from kafka import KafkaProducer                                                                                         
from random import randint                                                                                              
from time import sleep                                                                                                  
import sys 
import os                                                                                                             
                                                                                                                        
BROKER = 'localhost:9092'                                                                                               
TOPIC = 'housingprice'                                                                                                      
                                                                                                                        
TEST_FILE = os.path.abspath('data/for_stream_train.csv')                                                                                    
RECORDS = open(TEST_FILE).read().splitlines()                                                                             
                                                                                                                        
try:                                                                                                                    
    p = KafkaProducer(bootstrap_servers=BROKER)                                                                         
except Exception as e:                                                                                                  
    print(f"ERROR --> {e}")                                                                                             
    sys.exit(1)                                                                                                        
                                                                                                                        
while True:                                                                                                             
    message= RECORDS[randint(0, len(RECORDS)-1)]                                                               
    print(f">>> '{message}'")                                                                                           
    p.send(TOPIC, bytes(message, encoding="utf8"))                                                                      
    sleep(randint(1,4))