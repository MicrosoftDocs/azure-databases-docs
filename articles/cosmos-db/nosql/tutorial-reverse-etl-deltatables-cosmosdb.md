---
title: 'Tutorial: Reverse ETL (Extract Transform & Load) to Azure Cosmos DB from Delta Tables'
titleSuffix: Reverse ETL to Azure Cosmos DB for NoSQL
description: Reverse ETL moves data from your data lake layer (like Delta Lake in Databricks, Fabric) back into operational systems such as Azure Cosmos DB NoSQL using Cosmos DB Spark OLTP (Online Transaction Processing) connector. 
author: rakhithejraj
ms.author: rakhithejraj
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.custom: devx-track-python
ms.topic: tutorial
ms.date: 04/15/2025
zone_pivot_groups: programming-languages-spark-all-minus-sql-r-csharp
---

# Tutorial: Reverse ETL from Delta Lake to Cosmos DB with Spark OLTP Connector

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

## Reverse ETL Overview

  **What is Reverse ETL?**  
  Reverse ETL moves data from your Datawarehouses or data lake layer (like Delta Lake in Databricks, Fabric) back into operational systems. This data allows downstream apps to use the most recent, enriched data for real-time operational analytics.

  **Need for Reverse ETL**  
  Cloud data warehouses and data lakes have transformed data management, centralizing information and enabling powerful analytics. But the real value of data lies in turning insights into real-world decisions and customer experiences. To achieve this, clean, reliable data must move out of the warehouse / data lakes into operational systems. 
  
  Reverse ETL plays a crucial role in unlocking the full potential of your data assets by bridging the gap between analytics and operations, enabling better decision-making.

  **Reverse ETL Architecture**  
  The Reverse ETL layer depcited below is powered by Databricks and Apache Spark. It extracts cleansed and enriched data (e.g., Delta Tables), and writes it back into operational stores in Cosmos DB. This process enables:
  - **Real-Time Decisions:** Apps get access to the freshest data without relying on analysts or SQL.
  - **Data Activation:** Insights are pushed where they’re needed—not just in dashboards.
  - **Unified Source of Truth:** Delta Lake acts as the canonical layer, ensuring consistency across systems.

  :::image type="content" source="./media/cosmosdbingestion/reverseetl.png" lightbox="./media/cosmosdbingestion/reverseetl.png" alt-text="Reverse ETL Achitecture":::

  **Why Reverse ETL to Cosmos DB?**  
  Azure Cosmos DB is designed for ultra-low latency, global distribution, and NoSQL scalability, making it ideal for real-time applications.

  With Reverse ETL, you can sync Delta-enriched data into Cosmos DB, enabling real-time operational analytics. Push data like product catalogs, personalized customer info, pricing updates, inventory data, and feature recommendations into Cosmos DB, empowering downstream apps to make data-driven decisions instantly.

## Reverse ETL Data Load Stages

In this tutorial, you learn how to:

> [!div class="checklist"]
> - Set up a reverse ETL pipeline to move data from Delta tables in Databricks to Azure Cosmos DB NoSQL.
> - Configure Cosmos DB connection using the Cosmos DB Spark Connector.
> - Implement throughput control to limit Request Units (RUs) consumed by Spark jobs and manage the throughput for efficient data ingestion.
> - Perform initial data load from Delta tables to Cosmos DB.
> - Enable Change Data Capture (CDC) for real-time data synchronization.
> - Sync data using batch or streaming modes for efficient updates.
> - Query data from Cosmos DB for verification and analysis.

## Reverse ETL Data Load Best Practices 

## Prerequisites for Reverse ETL Pipeline

- An existing Azure Cosmos DB for NoSQL account.
  - You can create a new Cosmos DB account by following steps here, [create a new account](how-to-create-account.md?tabs=azure-portal).
- An existing Azure Databricks workspace.
  - You can create a new Azure Databricks workspace by following steps here,  [create a new Azure Databricks workspace](/azure/databricks/getting-started/).
- Setting up Managed Identity (AAD) based authentication to write to Cosmos DB using  Databricks

  - Managed Identity enables secure, passwordless authentication to Azure Cosmos DB from Databricks without managing secrets or keys.Perform these 4 steps to faciliate Managed Identity based authentication:

    **a. Get the Managed Identity Object ID (dbmanagedidentity)**
    This identity is used by Databricks when authenticating to Cosmos DB. This can be obtained either from Azure portal or CLI:

    In Azure portal, go to the Azure Databricks workspace, open the Managed Resource Group under Overview, select dbmanagedidentity resource, and copy its Object ID (Principal ID) from the Overview tab.

    ```azurecli

    az resource show --name dbmanagedidentity --resource-group <your-managed-resource-group> --namespace Microsoft.ManagedIdentity --resource-type "userAssignedIdentities" --query "properties.principalId" --output tsv

    ```

    **b. Assign Cosmos DB Data Plane Role (Built-in Data Contributor)**
    This data plane role grants the managed identity permission to read and write data in Cosmos DB containers. You can grant this role using this CLI command

    ```azurecli
    az cosmosdb sql role assignment create --account-name <your-cosmos-account-name> --resource-group <your-cosmos-rg> --scope "/" --principal-id <object-id-from-step a> --role-definition-id "00000000-0000-0000-0000-000000000002"

    ```

    **c. Assign Cosmos DB Control Plane Role (IAM)**
    This control plane role allows the managed identity to access account metadata (required for the Spark connector to initialize).

    You can assign this role in Azure portal. Go to Cosmos DB Account → Access Control (IAM) → Select Add → Add role assignment → Select Cosmos DB Account Reader Role  → Next  →  Assign access to "User, group, or service principal" →  select "select members" and add the dbmanagedidentity obtained from Step a  → select Review + Assign

    **d. Get Your Tenant ID (for AAD Auth)**
    This identifies your Azure Active Directory (AAD/Entra) instance. It's required by the Spark connector when using Managed Identity. You can obtain the Tenant ID using this CLI command

    ```azurecli
    az account show --query tenantId --output tsv

    ```

    This Tenant ID is one of the config inputs in the **Set Cosmos DB Configuration step** for the final configuration of Managed Identity. 

  If you're performing one-time testing using keys, the above four steps for setting up Managed Identity can be temporarily skipped. 


## Detailed Steps and Sample Code to Setup Reverse ETL Pipeline

In this tutorial, we set up a reverse ETL pipeline to move enriched data from Delta tables in Databricks to Azure Cosmos DB NoSQL. We use the Cosmos DB OLTP Spark Connector for batch or streaming data synchronization, ensuring data is available instantly for operational use.

**Step 1: Set Up Spark and Connector in Databricks**

  a. Create a Cluster:
  Open your Azure Databricks workspace.
  Create a new cluster with Runtime version 15.4 which has Long Term Support (Spark 3.5.0, Scala 2.12).

  b. Install the Cosmos DB Spark Connector:
  Go to Libraries > Install New > Maven.
  Use: Group ID: com.azure.cosmos.spark, Artifact ID: azure-cosmos-spark_3-5_2-12

  c. Create a Notebook:
  Go to Workspace > Your Folder > New > Notebook.
  Set the default language to Python or Scala and attach it to the cluster.

**Step 2: Set Cosmos DB Configuration**

Define a configuration dictionary (cosmos_config) in your notebook to connect your Spark session with Cosmos DB. These details include the Cosmos DB account endpoint, Managed Identity, Subscription, Tenant, database, and container name. It also enables throughput control to limit the RU consumption from Spark jobs, which helps prevent overloading the Cosmos DB account. Throughput control options include the control name and RU threshold. Target Throughput Threshold of 0.30 indicates that 30% of the allocated RUs on the target Cosmos DB container **products** is available for the spark operations.

::: zone pivot="programming-language-python"

```python
# Set configuration settings
cosmos_config = {
  # Generic Cosmos DB config settings
  "spark.cosmos.accountEndpoint": "<endpoint>",
  "spark.cosmos.database": "cosmicworks",
  "spark.cosmos.container": "products",
  # Managed Identity Based Cosmos DB config settings
  "spark.cosmos.auth.type":"ManagedIdentity",
  "spark.cosmos.account.subscriptionId": "<subscriptionId>",
  "spark.cosmos.account.tenantId": "<tenantId>",
  "spark.cosmos.account.resourceGroupName":"<resourceGroupName>",
  # Key Based Cosmos DB config settings for one-time testing
  # "spark.cosmos.accountKey": "<nosql-account-key>",
  # Throughput control based Cosmos DB config settings for managing the RU used by Spark
  "spark.cosmos.throughputControl.enabled": "true",
  "spark.cosmos.throughputControl.name": "TargetContainerThroughputControl",
  "spark.cosmos.throughputControl.targetThroughputThreshold": "0.30", 
  "spark.cosmos.throughputControl.globalControl.useDedicatedContainer": "false"
  }
```
::: zone-end

::: zone pivot="programming-language-scala"

```scala
// Set configuration settings
  val cosmosconfig = Map(
  // Generic Cosmos DB config settings
  "spark.cosmos.accountEndpoint" -> "<endpoint>",
  "spark.cosmos.database" -> "cosmicworks",
  "spark.cosmos.container" -> "products",
  // Managed Identity Based Cosmos DB config settings
  "spark.cosmos.auth.type"-> "ManagedIdentity",
  "spark.cosmos.account.subscriptionId" -> "<subscriptionId>",
  "spark.cosmos.account.tenantId" -> "<tenantId>",
  "spark.cosmos.account.resourceGroupName" -> "<resourceGroupName>",
  // Key Based Cosmos DB config settings for one-time testing
  // "spark.cosmos.accountKey" -> "<nosql-account-key>",
  // Throughput control based Cosmos DB config settings for managing the RU used by Spark
  "spark.cosmos.throughputControl.enabled" -> "true",
  "spark.cosmos.throughputControl.name" -> "TargetContainerThroughputControl",
  "spark.cosmos.throughputControl.targetThroughputThreshold" -> "0.30", 
  "spark.cosmos.throughputControl.globalControl.useDedicatedContainer" -> "false"
)
```

::: zone-end

**Step 3: Ingest Sample Product Data to Delta Table**

Create a sample DataFrame with product information and write it into a Delta table named products_delta. This step simulates curated, transformed data in your data lake that you intend to sync to Cosmos DB. Writing to Delta ensures you can later enable change data capture (CDC) for incremental syncs.

::: zone pivot="programming-language-python"

```python
# Ingest Sample Product Data to Delta Table
from pyspark.sql import SparkSession

# Create sample data and convert it to a DataFrame
df = spark.createDataFrame([
    ("p001", "Contoso Coffee Mug", "drinkware", 12.95),
    ("p002", "Contoso T-Shirt", "apparel", 19.99)
], ["id", "name", "category", "price"])

# Write the DataFrame to a Delta table
df.write.mode("append").format("delta").saveAsTable("products_delta")
```

::: zone-end

::: zone pivot="programming-language-scala"

```scala
// Ingest Sample Product Data to Delta Table
// Create sample data as a sequence and convert it to a DataFrame
val df = Seq(
  ("p001", "Contoso Coffee Mug", "drinkware", 12.95),
  ("p002", "Contoso T-Shirt", "apparel", 19.99)
).toDF("id", "name", "category", "price") 

// Write the DataFrame to a Delta table
df.write.mode("append").format("delta").saveAsTable("products_delta")
```

::: zone-end

**Step 4: Initial Batch Load to Cosmos DB**

Read the products_delta Delta table into a Spark DataFrame and perform an initial batch write to Cosmos DB using the cosmos.oltp format. Use the append mode to add the data without overwriting existing content in Cosmos DB. This step ensures that all the baseline data is available in Cosmos DB before CDC begins

::: zone pivot="programming-language-python"

```python
# Initial Batch Load to Cosmos DB
# Read the Delta table into a DataFrame
df_delta = spark.read.format("delta").table("products_delta")

# Write the DataFrame to Cosmos DB using the Cosmos OLTP format
df_delta.write.format("cosmos.oltp").mode("append").options(**cosmos_config).save()
```

::: zone-end

::: zone pivot="programming-language-scala"

```scala
// Initial Batch Load to Cosmos DB
// Read the Delta table into a DataFrame
val df_delta = spark.read.format("delta").table("products_delta")

// Write the DataFrame to Cosmos DB using the Cosmos OLTP format
df_delta.write.format("cosmos.oltp").mode("append").options(cosmosconfig).save()
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
// Enable CDC for the Delta table
spark.sql("""
  ALTER TABLE products_delta SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")
```

::: zone-end

**Step 6: Perform Change Data Capture (CDC) Reads from Delta Table**

After the historical data load, changes in the Delta table can be captured using Delta Change Data Feed (CDF). You can implement either batch-based or streaming-based CDC.

  **Step 6a: Batch CDC Sync to Cosmos DB**

  Runs on a schedule (for example, daily or hourly) and loads an incremental snapshot of the data based on changes captured since the last version or timestamp. To avoid data inconsistencies when large incremental volumes are being loaded from Delta tables to Cosmos DB, it is recommended to switch from the old Cosmos DB snapshot to the new one. For example, by writing to a new container or using a version flag, then flipping a pointer once the new data is fully loaded.

  Read the changes from the Delta table starting from a specific version or specific timestamp using the readChangeData option. Write the resulting changes to Cosmos DB using the same connector and configuration. The selected version number or timestamp needs to be after the change data feed enablement of delta table.

  ::: zone pivot="programming-language-python"

  ```python
  # Batch CDC Sync to Cosmos DB
  # Read the Change Data Capture (CDC) data from the Delta table
  cdc_batch_df = spark.read.format("delta").option("readChangeData", "true").option("startingVersion", "1").table("products_delta")

  # Write the captured changes to Cosmos DB in append mode
  cdc_batch_df.write.format("cosmos.oltp").mode("append").options(**cosmos_config).save()
  ```

  ::: zone-end

  ::: zone pivot="programming-language-scala"

  ```scala
  // Batch CDC Sync to Cosmos DB
  // Read the Change Data Capture (CDC) data from the Delta table
  val cdc_batch_df = spark.read.format("delta").option("readChangeData", "true").option("startingVersion", "1").table("products_delta")

  // Write the captured changes to Cosmos DB in append mode
  cdc_batch_df.write.format("cosmos.oltp").mode("append").options(cosmos_config).save()
  ```

  ::: zone-end

  **Step 6b: Stream CDC to Cosmos DB**

  Continuously syncs incremental changes in near real-time, keeping the target system up to date with minimal lag. Use spark Structured Streaming to continuously capture and write changes. The Delta table acts as a streaming source with readChangeData = true, and the Cosmos DB connector acts as a streaming sink. Specify a checkpoint location to ensure progress is tracked and duplicate writes are avoided.

  ::: zone pivot="programming-language-python"

  ```python
  # Stream CDC to Cosmos DB
  # Read Change Data Capture (CDC) stream from the Delta table 'products_delta'
  cdc_stream_df = spark.readStream.format("delta").option("readChangeData", "true").table("products_delta")

  # Write the CDC stream to Azure Cosmos DB using the OLTP connector with checkpointing
  streaming_query = cdc_stream_df.writeStream.format("cosmos.oltp").outputMode("append").options(**cosmos_config).option("checkpointLocation", "/mnt/checkpoints/products-stream").start()

  # Wait for the stream to terminate or time out after 60 seconds
  try:   streaming_query.awaitTermination(60)
  except:     print("Stream stopped or timed out.")

  # Stop the stream if it’s still running after the timeout
  if streaming_query.isActive: streaming_query.stop()
  ```

  ::: zone-end

  ::: zone pivot="programming-language-scala"

  ```scala
  # Stream CDC to Cosmos DB
  // Read Change Data Capture (CDC) stream from the Delta table 'products_delta'
  val cdcStreamDF = spark.readStream.format("delta").option("readChangeData", "true").table("products_delta")

  // Write the CDC stream to Azure Cosmos DB using the OLTP connector with checkpointing
  val streamingQuery = cdcStreamDF.writeStream.format("cosmos.oltp").outputMode("append").options(cosmosconfig).option("checkpointLocation", "/mnt/checkpoints/products-stream").start()

  // Wait for the stream to terminate or time out after 60 seconds
  try {
    streamingQuery.awaitTermination(60000) // time out in milli seconds
  } catch {
    case e: Exception => println("Stream stopped or timed out.")
  }
  // Stop the stream if it’s still running after the timeout
  if (streamingQuery.isActive) {
    streamingQuery.stop()
  }
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
val dfCosmos = spark.read.format("cosmos.oltp").options(cosmosConfig).load()
dfCosmos.select("id", "name", "category", "price").show()
```

::: zone-end
    
## Related content

- [Apache Spark](https://spark.apache.org/)
- [Azure Cosmos DB Spark Connector](/azure/cosmos-db/nosql/tutorial-spark-connector)
- [Throughput Control](/azure/cosmos-db/nosql/throughput-control-spark)
- [Azure Cosmos DB Partitioning and Partition Key Recommendation](/azure/cosmos-db/partitioning-overview)
- [AAD authentication in Apache Spark](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/cosmos/azure-cosmos-spark_3_2-12/docs/AAD-Auth.md)
- [Data Plane Role Based Access Control](/azure/cosmos-db/nosql/security/how-to-grant-data-plane-role-based-access)

