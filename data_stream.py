import logging
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as psf

BROKER_URL = "localhost:9092"
TOPIC_NAME = "com.udacity.phuri.kafka.sfcrime.callsforservice"

schema = StructType([StructField("crime_id", LongType(), True),
                     StructField("original_crime_type_name", StringType(), True),
                     StructField("report_date", DateType(), True),
                     StructField("call_date", DateType(), True),
                     StructField("offense_date", DateType(), True),
                     StructField("call_time", StringType(), True),
                     StructField("call_date_time", StringType(), True),
                     StructField("disposition", StringType(), True),
                     StructField("address", StringType(), True),
                     StructField("city", StringType(), True),
                     StructField("state", StringType(), True),
                     StructField("agency_id", IntegerType(), True),
                     StructField("address_type", StringType(), True),
                     StructField("common_location", StringType(), True)
                     ])


def run_spark_job(spark):
    # Create Spark configurations with max offset of 200 per trigger
    # set up correct bootstrap server and port
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", BROKER_URL) \
        .option("subscribe", TOPIC_NAME) \
        .option("startingOffsets", "earliest") \
        .option("maxRatePerPartition", 100) \
        .option("maxOffsetsPerTrigger", 200) \
        .load()

    # Show schema for the incoming resources for checks
    df.printSchema()

    # Take only value and convert it to String
    kafka_df = df.selectExpr("CAST(value AS STRING)")

    service_table = kafka_df \
        .select(psf.from_json(psf.col('value'), schema).alias("cfs")) \
        .select("cfs.*")

    # select original_crime_type_name and disposition
    distinct_table = service_table.select(psf.to_timestamp(service_table.call_date_time).alias("call_date_time"),
                                          service_table.original_crime_type_name,
                                          service_table.disposition)

    # count the number of original crime type
    agg_df = distinct_table.select(distinct_table.call_date_time,
                                   distinct_table.original_crime_type_name,
                                   distinct_table.disposition
                                   ) \
        .withWatermark("call_date_time", "60 minutes") \
        .groupBy(
        psf.window(distinct_table.call_date_time, "10 minutes", "5 minutes"),
        psf.col("original_crime_type_name")
    ) \
        .count()

    # Q1. Submit a screenshot of a batch ingestion of the aggregation
    # write output stream
    query = agg_df \
        .writeStream \
        .format("console") \
        .outputMode("complete") \
        .start()

    # attach a ProgressReporter
    query.awaitTermination()

    # get the right radio code json path
    radio_code_json_filepath = "radio_code.json"
    radio_code_df = spark.read.json(radio_code_json_filepath)

    # clean up your data so that the column names match on radio_code_df and agg_df
    # we will want to join on the disposition code

    # rename disposition_code column to disposition
    radio_code_df = radio_code_df.withColumnRenamed("disposition_code", "disposition")

    # join on disposition column
    join_query = agg_df \
        .join(radio_code_df, "disposition") \
        .writeStream \
        .format("console") \
        .queryName("join") \
        .start()

    join_query.awaitTermination()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # Create Spark in Standalone mode
    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("KafkaSparkStructuredStreaming") \
        .getOrCreate()

    logger.info("Spark started")

    run_spark_job(spark)

    spark.stop()
