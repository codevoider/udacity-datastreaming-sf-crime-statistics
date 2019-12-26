# SF Crime Statistics using Kafka and Spark Streaming
As part of Udacity Data Streaming nanodegree, this project demonstrates how Kafka producer produces messages into the Kafka topic and how we integrate Kafka with Spark streaming based on Kaggle open data, [SF Police Calls for Service and Incidents](https://www.kaggle.com/san-francisco/sf-police-calls-for-service-and-incidents).

## Environment
- Java JDK 1.8
- Scala 2.13.1
- Spark 2.4.4
- Kafka 2.4.0
- Python 3.7.5

For Python libraries, refer to requirement.txt.

## How to run the application
*** Note that the data source files are required to run this repository.  Follow this data source download [link](https://drive.google.com/file/d/1FqsGfUiczZkGUCqzo8otwKLcIa9n--3-/view?usp=sharing), and unzip into the root folder.

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


## Q&A from Udacity Data Streaming Nanodegree

#### 1. How did changing values on the SparkSession property parameters affect the throughput and latency of the data?

Changing values on the SparkSession may result in increasing or decreasing throughput and latency of the data.  We can check `processedRowsPerSecond` and `inputRowsPerSecond` on the progress report. 

#### 2. What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?

For data receiving, one of the most efficient SparkSession properties I think is `spark.executor.cores` which needs to be set accordingly to the Kafka topic partitions so that the pipeline will not have any idle core (in case, set it more than Kafka partitions) or bottleneck (in case, set it less than Kafka partitions).

The second one is `spark.streaming.kafka.maxRatePerPartition`.  The value can be increased if it is capped to increase ingestion rate.

The third one I think is `spark.default.parallelism` which Spark Tuning Guide recommended should be set to 2-3 per CPU cores.  Except from relying on `processedRowsPerSecond` on the progress report alone, we can monitor the CPU core utilization on any OS, and see if the parellelism value can push it up to the desired level.
