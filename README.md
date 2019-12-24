# SF Crime Statistics using Kafka and Spark Streaming
as part of Udacity Data Streaming nanodegree

## Environment
- Java JDK 1.8
- Scala
- Spark (using 2.4.4)

For Python libraries, refer to requirement.txt.

## How to run the application
*** Note that the data source files are required to run this repository.

#### 1. Start Zookeeper.

`zookeeper-server-start config/zookeeper.properties`

#### 2. Start Kafka server.

`kafka-server-start config/server.properties`

#### 3. Start Kafka Producer.

`python kafka_server.py`

#### 4. Run the following command to consume messages.

`kafka-console-consumer --topic com.udacity.phuri.kafka.sfcrime.callsforservice --from-beginning --bootstrap-server localhost:9092`

#### 5. Submit spark job.

`spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.4 --master local[*] data_stream.py`
*** Note that 2.4.4 is the version of spark installed.


## Q&A

#### 1. How did changing values on the SparkSession property parameters affect the throughput and latency of the data?


#### 2. What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?

