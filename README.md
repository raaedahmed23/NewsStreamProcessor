# NewsStreamProcessor
An integrated data pipeline that fetches, processes, and visualizes real-time news data using Apache Kafka, Spark, and the ELK stack, focusing on named entity extraction and trend analysis.

0. Download Kafka in the project folder 

1. Start Zookeeper and Kafka service by running the commands in different terminals:
```console
	- bin/zookeeper-server-start.sh config/zookeeper.properties
	- bin/kafka-server-start.sh config/server.properties
```

   Create two kafka topics by the name 'rawdata' and 'processed'

```console
	- bin/kafka-topics.sh --create --topic rawdata --bootstrap-server localhost:9092
	- bin/kafka-topics.sh --create --topic processed --bootstrap-server localhost:9092
```

2. Set up the ELK stack which is deployed using docker: 
```console
	- cd elk
```
	
Make changes to the logstash.conf file at line 3 to the IP address of your system.

```console
	- docker-compose up -d
```

3. Run producer.py to start fetching news sentences and write to the first topic:
```console
	- python producer.py
```

4. Run the spark program ner.py to read information from the topic 'rawdata' and write the counts of named entities to 'processed'
```console
	- spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 ner.py localhost:9092 subscribe rawdata
```

5. Access Kibana at localhost:5601, create a visualization with named_entities on horizontal axis and counts on vertical axis