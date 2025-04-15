---
title: 'Tutorial: Reverse ETL (Extract Transform & Load) to Azure Cosmos DB NoSQL from Delta Tables using Azure Databricks'
titleSuffix: Reverse ETL to Azure Cosmos DB for NoSQL
description: Reverse ETL moves data from your data lake layer (like Delta Lake in Databricks, Fabric) back into operational systems such as Azure Cosmos DB NoSQL using Cosmos DB Spark OLTP (Online Transaction Processing) connector. 
author: rakhithejraj
ms.author: rakhithejraj
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.custom: devx-track-python
ms.topic: tutorial
ms.date: 04/17/2025
zone_pivot_groups: programming-languages-spark-all-minus-sql-r-csharp
---

# Tutorial: Reverse ETL to Azure Cosmos DB NoSQL from Delta Tables using Azure Databricks

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

## What is Reverse ETL?
Reverse ETL moves data from your analytics or data lake layer (like Delta Lake in Databricks, Fabric) back into operational systems such as Azure Cosmos DB for NoSQL. This data allows downstream apps to use the most recent, transformed data for real-time operations.

## Why Reverse ETL to Cosmos DB?
Azure Cosmos DB is optimized for ultra-low latency reads and writes, global distribution, and NoSQL scale and flexibility. You can use reverse ETL to sync Delta-enriched data like product catalogs, customer personalization, pricing or inventory updates, and real-time operational metrics.

In this tutorial, you learn how to:

> [!div class="checklist"]
> - Set up a reverse ETL pipeline to move data from Delta tables in Databricks to Azure Cosmos DB NoSQL.
> - Configure Cosmos DB connection using the Cosmos DB Spark Connector.
> - Implement throughput control to limit Request Units (RUs) consumed by Spark jobs and manage the throughput for efficient data ingestion.
> - Perform initial data load from Delta tables to Cosmos DB.
> - Enable Change Data Capture (CDC) for real-time data synchronization.
> - Sync data using batch or streaming modes for efficient updates.
> - Query data from Cosmos DB for verification and analysis.

## Prerequisites

- An existing Azure Cosmos DB for NoSQL account.
  - You can create a new Cosmos DB account by following steps here, [create a new account](how-to-create-account.md?tabs=azure-portal).
  - No Azure subscription? You can [try Azure Cosmos DB free](../try-free.md) with no credit card required.
- An existing Azure Databricks workspace.
  - You can create a new Azure Databricks workspace by following steps here,  [create a new Azure Databricks workspace](/azure/databricks/getting-started/).

## Detailed Steps and Sample Code to Setup Reverse ETL Pipeline

In this tutorial, we set up a reverse ETL pipeline to move enriched data from Delta tables in Databricks to Azure Cosmos DB NoSQL. We use the Cosmos DB OLTP Spark Connector for batch or streaming data synchronization, ensuring data is available instantly for operational use.

**Step 1: Set Up Spark and Connector in Databricks**

1. Create a Cluster:
Open your Azure Databricks workspace.
Create a new cluster with Runtime version 15.4 which has Long Term Support (Spark 3.5.0, Scala 2.12).

1. Install the Cosmos DB Spark Connector:
Go to Libraries > Install New > Maven.
Use: Group ID: com.azure.cosmos.spark, Artifact ID: azure-cosmos-spark_3-5_2-12

1. Create a Notebook:
Go to Workspace > Your Folder > New > Notebook.
Set the default language to Python or Scala and attach it to the cluster.

**Step 2: Set Cosmos DB Configuration**

Define a configuration dictionary (cosmos_config) in your notebook to connect your Spark session with Cosmos DB. These details include the Cosmos DB account endpoint, Managed Identity, Subscription, Tenant, database, and container name. It also enables throughput control to limit the RU consumption from Spark jobs, which helps prevent overloading the Cosmos DB account. Throughput control options include the control name, RU threshold, and the metadata container details

::: zone pivot="programming-language-python"

```python
# Set configuration settings
  cosmos_config = {
  "spark.cosmos.accountEndpoint": "<nosql-account-endpoint>",
  "spark.cosmos.accountKey": "<nosql-account-key>",
  #"spark.cosmos.account.subscriptionId": subscriptionId,
  #"spark.cosmos.account.tenantId": tenantId,
  #"spark.cosmos.account.resourceGroupName":resourceGroupName,
  "spark.cosmos.database": "cosmicworks",
  "spark.cosmos.container": "products",
  "spark.cosmos.throughputControl.enabled": "true",
  "spark.cosmos.throughputControl.name": "TargetContainerThroughputControl",
  "spark.cosmos.throughputControl.targetThroughputThreshold": "0.30", 
  "spark.cosmos.throughputControl.globalControl.useDedicatedContainer": "false"
  }
```
::: zone-end

::: zone pivot="programming-language-scala"

```scala
# Set configuration settings
val config = Map(
  "spark.cosmos.accountEndpoint" -> "<nosql-account-endpoint>",
  "spark.cosmos.accountKey" -> "<nosql-account-key>",
  "spark.cosmos.database" -> "cosmicworks",
  "spark.cosmos.container" -> "products"
)
```

::: zone-end

**Step 3: Ingest Sample Product Data to Delta Table**

Create a sample DataFrame with product information and write it into a Delta table named products_delta. This step simulates curated, transformed data in your data lake that you intend to sync to Cosmos DB. Writing to Delta ensures you can later enable change data capture (CDC) for incremental syncs.

::: zone pivot="programming-language-python"

```python
# Ingest Sample Product Data to Delta Table
from pyspark.sql import SparkSession
df = spark.createDataFrame([
    ("p001", "Contoso Coffee Mug", "drinkware", 12.95),
    ("p002", "Contoso T-Shirt", "apparel", 19.99)
], ["id", "name", "category", "price"])
df.write.mode("append").format("delta").saveAsTable("products_delta")
```

::: zone-end

::: zone pivot="programming-language-scala"

```scala
# Ingest Sample Product Data to Delta Table
val config = Map(
  "spark.cosmos.accountEndpoint" -> "<nosql-account-endpoint>",
  "spark.cosmos.accountKey" -> "<nosql-account-key>",
  "spark.cosmos.database" -> "cosmicworks",
  "spark.cosmos.container" -> "products"
)
```

::: zone-end

**Step 4: Initial Batch Load to Cosmos DB**

Read the products_delta Delta table into a Spark DataFrame and perform an initial batch write to Cosmos DB using the cosmos.oltp format. Use the append mode to add the data without overwriting existing content in Cosmos DB. This step ensures that all the baseline data is available in Cosmos DB before CDC begins

::: zone pivot="programming-language-python"

```python
# Initial Batch Load to Cosmos DB
df_delta = spark.read.format("delta").table("products_delta")
df_delta.write.format("cosmos.oltp") .mode("append").options(**cosmos_config) .save()
```

::: zone-end

::: zone pivot="programming-language-scala"

```scala
# Initial Batch Load to Cosmos DB
val config = Map(
  "spark.cosmos.accountEndpoint" -> "<nosql-account-endpoint>",
  "spark.cosmos.accountKey" -> "<nosql-account-key>",
  "spark.cosmos.database" -> "cosmicworks",
  "spark.cosmos.container" -> "products"
)
```

::: zone-end

**Step 5: Enable Change Data Feed for Delta table**

Enable Delta Lake's Change Data Feed on the products_delta table by altering its table properties. CDF allows Delta to track all future row-level inserts, updates, and deletes. Enabling this property is essential for performing incremental syncs to Cosmos DB, as it exposes changes without needing to compare snapshots.


::: zone pivot="programming-language-python"

```python
# Enable CDC for Delta table
spark.sql("""
  ALTER TABLE products_delta SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")
```

::: zone-end

::: zone pivot="programming-language-scala"

```scala
# Enable CDC for Delta table
val config = Map(
  "spark.cosmos.accountEndpoint" -> "<nosql-account-endpoint>",
  "spark.cosmos.accountKey" -> "<nosql-account-key>",
  "spark.cosmos.database" -> "cosmicworks",
  "spark.cosmos.container" -> "products"
)
```

::: zone-end

**Step 6: Perform Change Data Capture (CDC) Reads from Delta Table**

After the historical data load, changes in the Delta table can be captured using Delta Change Data Feed (CDF). You can implement either batch-based or streaming-based CDC.

**Step 6a: Batch CDC Sync to Cosmos DB**

Runs on a schedule (for example, daily or hourly) and loads an incremental snapshot of the data based on changes captured since the last version or timestamp. To avoid data inconsistencies when large incremental volumes are being loaded from Delta tables to Cosmos DB, there has to be a way to atomically switch from the old Cosmos DB snapshot to the new one. For example, by writing to a new container or using a version flag, then flipping a pointer once the new data is fully loaded.

Read the changes from the Delta table starting from a specific version or specific timestamp using the readChangeData option. Write the resulting changes to Cosmos DB using the same connector and configuration.

::: zone pivot="programming-language-python"

```python
# Batch CDC Sync to Cosmos DB
cdc_batch_df = spark.read.format("delta").option("readChangeData", "true").option("startingVersion", "1").table("products_delta")
cdc_batch_df.write.format("cosmos.oltp").mode("append").options(**cosmos_config).save()
```

::: zone-end

::: zone pivot="programming-language-scala"

```scala
# Batch CDC Sync to Cosmos DB
val config = Map(
  "spark.cosmos.accountEndpoint" -> "<nosql-account-endpoint>",
  "spark.cosmos.accountKey" -> "<nosql-account-key>",
  "spark.cosmos.database" -> "cosmicworks",
  "spark.cosmos.container" -> "products"
)
```

::: zone-end

**Step 6b: Stream CDC to Cosmos DB**

Continuously syncs incremental changes in near real-time, keeping the target system up to date with minimal lag. Use spark Structured Streaming to continuously capture and write changes. The Delta table acts as a streaming source with readChangeData = true, and the Cosmos DB connector acts as a streaming sink. Specify a checkpoint location to ensure progress is tracked and duplicate writes are avoided.

::: zone pivot="programming-language-python"

```python
# Stream CDC to Cosmos DB
cdc_stream_df = spark.readStream.format("delta").option("readChangeData", "true").table("products_delta")
streaming_query = cdc_stream_df.writeStream.format("cosmos.oltp").outputMode("append").options(**cosmos_config).option("checkpointLocation", "/mnt/checkpoints/products-stream").start()
try:   streaming_query.awaitTermination(60)
except:     print("Stream stopped or timed out.")
if streaming_query.isActive: streaming_query.stop()
```

::: zone-end

::: zone pivot="programming-language-scala"

```scala
# Stream CDC to Cosmos DB
val config = Map(
  "spark.cosmos.accountEndpoint" -> "<nosql-account-endpoint>",
  "spark.cosmos.accountKey" -> "<nosql-account-key>",
  "spark.cosmos.database" -> "cosmicworks",
  "spark.cosmos.container" -> "products"
)
```

::: zone-end

**Step 7: Query Cosmos DB from Spark**

After writing to Cosmos DB, verify the data by reading it back into Spark using the same Cosmos DB configuration. Then inspect the ingested data, run validations, or join with other datasets in Delta for analytics or reporting. Cosmos DB supports fast, indexed reads for real-time query performance.

::: zone pivot="programming-language-python"

```python
# Query Cosmos DB from Spark
df_cosmos = spark.read.format("cosmos.oltp").options(**cosmos_config).load()
df_cosmos.select("id", "name", "category", "price").show()
```

::: zone-end

::: zone pivot="programming-language-scala"

```scala
# Query Cosmos DB from Spark
val config = Map(
  "spark.cosmos.accountEndpoint" -> "<nosql-account-endpoint>",
  "spark.cosmos.accountKey" -> "<nosql-account-key>",
  "spark.cosmos.database" -> "cosmicworks",
  "spark.cosmos.container" -> "products"
)
```

::: zone-end
    
## Related content

- [Apache Spark](https://spark.apache.org/)
- [Azure Cosmos DB Spark Connector](articles/cosmos-db/nosql/tutorial-spark-connector.md)
- [Throughput Control](articles\cosmos-db\nosql\throughput-control-spark.md)
- [Azure Cosmos DB Partitioning and Partition Key Recommendation](/azure/cosmos-db/partitioning-overview)
- [Azure Cosmos DB Partitioning and Partition Key Recommendation](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/cosmos/azure-cosmos-spark_3_2-12/docs/AAD-Auth.md)