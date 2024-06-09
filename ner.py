from __future__ import print_function
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, udf
from pyspark.sql.types import ArrayType, StringType
from pyspark.sql.functions import col
from pyspark.sql.types import StringTypegit

import spacy

outputTopic = "processed"


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("""
        Usage: ner.py <bootstrap-servers> <subscribe-type> <topics>
        """, file=sys.stderr)
        sys.exit(-1)

    bootstrapServers = sys.argv[1]
    subscribeType = sys.argv[2]
    topics = sys.argv[3]

    spark = SparkSession \
        .builder \
        .appName("NERCounter") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # Create DataSet representing the stream of input lines from kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", bootstrapServers) \
        .option(subscribeType, topics) \
        .option("startingOffsets", "earliest") \
        .load() \
        .selectExpr("CAST(value AS STRING)")
    
    
    nlp = spacy.load("en_core_web_sm")

    def extract_named_entities(text):
        if not text:
            return []
        try:
            doc = nlp(text)
            return [ent.text for ent in doc.ents]
        except Exception as e:
            print(f"Error processing text: {e}")
            return []
    
    # Register the User Defined Function
    extract_named_entities_udf = udf(extract_named_entities, ArrayType(StringType()))

    # Apply the function on the received data 
    df = df.withColumn("named_entities", extract_named_entities_udf(col("value")))

    # Explode to create individual rows
    df = df.select(explode(col("named_entities")).alias("named_entity"))
    
    # Group by named entity and count occurrences
    df_counts = df.groupBy("named_entity").count()

    query = df_counts.selectExpr("to_json(struct(*)) AS value").writeStream \
        .outputMode("complete") \
        .format("kafka") \
        .option("topic", outputTopic) \
        .option("kafka.bootstrap.servers", bootstrapServers) \
        .option("checkpointLocation", "./checkpoint") \
        .trigger(processingTime="30 seconds") \
        .start()

    query.awaitTermination()


