---
title: Change feed with Apache Spark
description: Learn how to use the Azure Cosmos DB Spark Connector to read the change feed, including pull model implementation, checkpointing, and scale-out processing.
author: TheovanKraay
ms.author: thvankra
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 08/15/2025
appliesto:
  - ✅ NoSQL
---

# Change feed with Apache Spark

The [Azure Cosmos DB Spark Connector](tutorial-spark-connector.md) provides a powerful way to process the change feed at scale using Apache Spark. The connector uses the Java SDK underneath and implements a [pull model](change-feed-pull-model.md) that distributes processing transparently across Spark executors, making it ideal for large-scale data processing scenarios.

## How the Spark Connector works

The Spark Connector for Azure Cosmos DB builds on top of the Azure Cosmos DB Java SDK and implements a pull model approach to reading the change feed. Key characteristics include:

- **Java SDK foundation**: Uses the robust Azure Cosmos DB Java SDK underneath for reliable change feed processing
- **Pull model implementation**: Follows the [change feed pull model](change-feed-pull-model.md) pattern, giving you control over the pace of processing
- **Distributed processing**: Automatically distributes change feed processing across multiple Spark executors for parallel processing
- **Transparent scaling**: The connector handles partitioning and load distribution without requiring manual intervention

## Unique checkpointing capability

One of the key advantages of using the Spark Connector for change feed processing is its built-in checkpointing mechanism. This feature provides:

- **Automatic recovery**: Out-of-the-box mechanism for recovery when processing change feed at scale
- **Fault tolerance**: Ability to resume processing from the last checkpoint in case of failures
- **State management**: Maintains processing state across Spark sessions and cluster restarts
- **Scalability**: Supports checkpointing across distributed Spark environments

This checkpointing capability is unique to the Spark Connector and isn't available when using the SDKs directly, making it especially valuable for production scenarios requiring high availability and reliability.

> [!WARNING]
> The `spark.cosmos.changeFeed.startFrom` configuration is ignored if there are existing bookmarks in the checkpoint location. When resuming from a checkpoint, the connector will continue from the last processed position rather than the specified start point.

## When to use Spark for change feed processing

Consider using the Spark Connector for change feed processing in these scenarios:

- **Large-scale data processing**: When you need to process high volumes of change feed data that exceed single-machine capabilities
- **Complex transformations**: When your change feed processing involves complex data transformations, aggregations, or joins with other datasets
- **Distributed analytics**: When you need to perform real-time or near-real-time analytics on change feed data across a distributed environment
- **Integration with data pipelines**: When change feed processing is part of larger ETL/ELT pipelines that already use Spark
- **Fault tolerance requirements**: When you need robust checkpointing and recovery mechanisms for production workloads
- **Multi-container processing**: When you need to process change feeds from multiple containers simultaneously

For simpler scenarios or when you need fine-grained control over individual document processing, consider using the [change feed processor](change-feed-processor.md) or [pull model](change-feed-pull-model.md) directly with the SDKs.

## Code examples

The following examples show how to read from the change feed using the Spark Connector. For more comprehensive examples, see the complete sample notebooks:

- [Python structured streaming sample](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/cosmos/azure-cosmos-spark_3/Samples/Python/NYC-Taxi-Data/02_StructuredStreaming.ipynb) - NYC Taxi data processing with change feed
- [Scala container migration sample](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/cosmos/azure-cosmos-spark_3/Samples/DatabricksLiveContainerMigration/CosmosDBLiveSingleContainerMigration.scala) - Live container migration using change feed

### [Python](#tab/python)

```python
# Configure change feed reading

changeFeedConfig = {
    "spark.cosmos.accountEndpoint": "https://<account-name>.documents.azure.com:443/",
    "spark.cosmos.accountKey": "<account-key>",
    "spark.cosmos.database": "<database-name>",
    "spark.cosmos.container": "<container-name>",
    # Start from beginning, now, or specific timestamp (ignored if checkpoints exist)
    "spark.cosmos.changeFeed.startFrom": "Beginning",  # "Now" or "2020-02-10T14:15:03"
    "spark.cosmos.changeFeed.mode": "LatestVersion",  # or "AllVersionsAndDeletes"
    # Control batch size - if not set, all available data processed in first batch
    "spark.cosmos.changeFeed.itemCountPerTriggerHint": "50000",
    "spark.cosmos.read.partitioning.strategy": "Restrictive"
}

# Read change feed as a streaming DataFrame
changeFeedDF = spark \
    .readStream \
    .format("cosmos.oltp.changeFeed") \
    .options(**changeFeedConfig) \
    .load()

# Configure output settings with checkpointing
outputConfig = {
    "spark.cosmos.accountEndpoint": "https://<target-account>.documents.azure.com:443/",
    "spark.cosmos.accountKey": "<target-account-key>",
    "spark.cosmos.database": "<target-database>",
    "spark.cosmos.container": "<target-container>",
    "spark.cosmos.write.strategy": "ItemOverwrite"
}

# Process and write the change feed data with checkpointing
query = changeFeedDF \
    .selectExpr("*") \
    .writeStream \
    .format("cosmos.oltp") \
    .outputMode("append") \
    .option("checkpointLocation", "/tmp/changefeed-checkpoint") \
    .options(**outputConfig) \
    .start()

# Wait for the streaming query to finish
query.awaitTermination()
```

### [Scala](#tab/scala)

```scala
// Configure change feed reading
val changeFeedConfig = Map(
    "spark.cosmos.accountEndpoint" -> "https://<account-name>.documents.azure.com:443/",
    "spark.cosmos.accountKey" -> "<account-key>",
    "spark.cosmos.database" -> "<database-name>",
    "spark.cosmos.container" -> "<container-name>",
    // Start from beginning, now, or specific timestamp (ignored if checkpoints exist)
    "spark.cosmos.changeFeed.startFrom" -> "Beginning", // "Now" or "2020-02-10T14:15:03"
    "spark.cosmos.changeFeed.mode" -> "LatestVersion", // or "AllVersionsAndDeletes"
    // Control batch size - if not set, all available data processed in first batch
    "spark.cosmos.changeFeed.itemCountPerTriggerHint" -> "50000",
    "spark.cosmos.read.partitioning.strategy" -> "Restrictive"
)

// Read change feed as a streaming DataFrame
val changeFeedDF = spark
    .readStream
    .format("cosmos.oltp.changeFeed")
    .options(changeFeedConfig)
    .load()

// Configure output settings with checkpointing
val outputConfig = Map(
    "spark.cosmos.accountEndpoint" -> "https://<target-account>.documents.azure.com:443/",
    "spark.cosmos.accountKey" -> "<target-account-key>",
    "spark.cosmos.database" -> "<target-database>",
    "spark.cosmos.container" -> "<target-container>",
    "spark.cosmos.write.strategy" -> "ItemOverwrite"
)

// Process and write the change feed data with checkpointing
val query = changeFeedDF
    .selectExpr("*")
    .writeStream
    .format("cosmos.oltp")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/changefeed-checkpoint")
    .options(outputConfig)
    .start()

// Wait for the streaming query to finish
query.awaitTermination()
```

---

## Key configuration options

When working with change feed in Spark, these configuration options are particularly important:

- **spark.cosmos.changeFeed.startFrom**: Controls where to start reading the change feed
  - `"Beginning"` - Start from the beginning of the change feed
  - `"Now"` - Start from the current time
  - `"2020-02-10T14:15:03"` - Start from a specific timestamp (ISO 8601 format)
  - **Note**: This setting is ignored if there are existing bookmarks in the checkpoint location
- **spark.cosmos.changeFeed.mode**: Specifies the change feed mode
  - `"LatestVersion"` - Process only the latest version of changed documents
  - `"AllVersionsAndDeletes"` - Process all versions of changes including deletes
- **spark.cosmos.changeFeed.itemCountPerTriggerHint**: Controls batch processing size
  - Approximate maximum number of items read from change feed for each micro-batch/trigger
  - Example: `"50000"` 
  - **Important**: If not set, all available data in the change feed will be processed in the first micro-batch
- **checkpointLocation**: Specifies where to store checkpoint information for fault tolerance and recovery
- **spark.cosmos.read.partitioning.strategy**: Controls how data is partitioned across Spark executors

## Next steps

- Learn more about [change feed design patterns](change-feed-design-patterns.md)
- Explore the [change feed pull model](change-feed-pull-model.md)
- Understand [change feed processor](change-feed-processor.md) for single-machine scenarios
- Review the [Spark Connector documentation](tutorial-spark-connector.md) for additional configuration options
- Check out [change feed modes](change-feed-modes.md) for different processing scenarios
