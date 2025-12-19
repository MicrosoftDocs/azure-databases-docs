---
title: Tutorial - Reverse extract, transform, & load (ETL)
description: Set up an extract, transform, and load (ETL) solution that moves data from a data lake layer back into operational system (database) layer for real-time analytics. 
author: rakhithejraj
ms.author: rakhithejraj
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.custom: devx-track-python
ms.topic: tutorial
ms.date: 04/21/2025
zone_pivot_groups: programming-languages-spark-all-minus-sql-r-csharp
appliesto:
  - ✅ NoSQL
---

# Tutorial: Reverse extract, transform, & load (ETL) from Delta Lake to Azure Cosmos DB for NoSQL with Spark OLTP connector

In this tutorial, you set up a reverse ETL pipeline to move enriched data from Delta tables in Azure Databricks to Azure Cosmos DB for NoSQL. You then use the Online Transaction Processing (OLTP) Spark connector for Azure Cosmos DB for NoSQL to synchronize data.

## Prerequisites for Reverse ETL pipeline setup

- An existing Azure Cosmos DB account.
  - If you have an Azure subscription, [create a new account](how-to-create-account.md?tabs=azure-portal).
- An existing Azure Databricks workspace.
  - If you have an Azure subscription, [create a new workspace](/azure/databricks/getting-started).
- Latest version of Azure CLI.
  - If you prefer, you can also use the [Azure Cloud Shell](/azure/cloud-shell/overview).

## Configure role-based access control with Microsoft Entra

Azure managed identities ensure secure, passwordless authentication to Azure Cosmos DB for NoSQL without manually managing credentials. In this prerequisite step, set up the user-assigned managed identity that Azure Databricks automatically creates with read access to metadata and write access to data for your Azure Cosmos DB for NoSQL account. This step configures both control and data plane role-based access control roles for the managed identity.

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. Navigate to the existing Azure Databricks resource.

1. In the **Essentials** pane, locate and navigate to the managed resource group associated with the workspace.

1. In the managed resource group, select the user-assigned managed identity that was automatically created with the workspace.

1. Record the value of the **Client ID** and **Object (principal) ID** fields in the **Essentials** pane. You use this value later to assign control and data plane roles.

    > [!TIP]
    > Alternatively, you can get the principal ID of the managed identity using the Azure CLI. Assuming that the managed identity's name is `dbmanagedidentity`, use the `az resource show` command to get the principal ID.
    >
    > ```azurecli-interactive
    > az resource show \
    >     --resource-group "<name-of-managed-resource-group>" \
    >     --name "dbmanagedidentity" \
    >     --resource-type "Microsoft.ManagedIdentity/userAssignedIdentities" \
    >     --query "{clientId: properties.clientId, principalId: properties.principalId}"
    > ```
    >

1. Navigate to the target Azure Cosmos DB for NoSQL account.

1. On the account's page, select **Access control (IAM)**.

1. In the **Access control** pane, select the **Add** and then the **Add role assignment** options to begin the process of assigning a control plane role to the user-assigned managed identity.

1. Select the **Cosmos DB Account Reader** role in the list of roles for assignment.

1. In the section to assign access to a **user, group, or service principal** interact with the **select members** option.

1. In the members dialog, enter the principal ID to filter to the user-assigned managed identity associated with Azure Databricks. **Select** that identity.

1. Finally, select **Review + Assign** to create the control plane role assignment.

1. Use the `az cosmosdb sql role assignment create` command to assign the `Cosmos DB Built-in Data Contributor` data plane role and the `/` scope to the user-assigned managed identity associated with Azure Databricks.

    ```azurecli-interactive
    az cosmosdb sql role assignment create \
        --resource-group "<name-of-resource-group>" \
        --account-name "<name-of-cosmos-nosql-account>" \
        --principal-id "<managed-identity-principal-id>" \
        --role-definition-name "Cosmos DB Built-in Data Contributor" \ --scope "/"
    ```

1. Use `az account show` to get your subscription and tenant identifiers. These values are required in a later step with the Spark connector using Microsoft Entra authentication.

    ```azurecli-interactive
    az account show --query '{subscriptionId: id, tenantId: tenantId}'
    ```

## Create a Databricks notebook



1. Navigate to the existing Azure Databricks resource and then open the workspace UI.

1. If you don't have a cluster already, create a new cluster.

    > [!IMPORTANT]
    > Ensure the cluster has Runtime version 15.4 of higher which has long-term support for Spark 3.5.0 and Scala 2.12. The remaining steps in this guide assume these versions of the tools.

1. Navigate to **Libraries** > **Install New** > and **Maven** to install a Maven package.

1. Search for the Spark connector for Azure Cosmos DB for NoSQL by using the **Group ID** filter `com.azure.cosmos.spark` and selecting the package with an **Artifact ID** of `azure-cosmos-spark_3-5_2-12`.

1. Create a new notebook by navigating to **Workspace** > ***\[Folder\]*** > **New** > **Notebook**.

1. Attach the notebook to your cluster.

## Configure Spark connector in Azure Databricks

Configure the Spark connector to connect to your account's container using Microsoft Entra authentication. Also, configure the connector to only use a limited threshold of throughput for Spark operations. To configure the spark connector, define a configuration dictionary with credentials to connect to your account. These credentials include:

| | Value |
| --- | --- |
| **`spark.cosmos.accountEndpoint`** | The NoSQL account endpoint  |
| **`spark.cosmos.database`** | The name of the target database |
| **`spark.cosmos.container`** | The name of the target container |
| **`spark.cosmos.auth.type`** | `ManagedIdentity`  |
| **`spark.cosmos.auth.aad.clientId`** | The **Client ID** of the user-assigned managed identity |
| **`spark.cosmos.account.subscriptionId`** | The ID of the subscription |
| **`spark.cosmos.account.tenantId`** | The ID of the associated Microsoft Entra tenant |
| **`spark.cosmos.account.resourceGroupName`** | The name of the resource group |
| **`spark.cosmos.throughputControl.enabled`** | `true` |
| **`spark.cosmos.throughputControl.name`** | `TargetContainerThroughputControl` |
| **`spark.cosmos.throughputControl.targetThroughputThreshold`** | `0.30` |
| **`spark.cosmos.throughputControl.globalControl.useDedicatedContainer`** | `false |

::: zone pivot="programming-language-python"

```python
cosmos_config = {
    # General settings
    "spark.cosmos.accountEndpoint": "<endpoint>",
    "spark.cosmos.database": "products",
    "spark.cosmos.container": "recommendations",
    # Entra authentication settings
    "spark.cosmos.auth.type": "ManagedIdentity",
    "spark.cosmos.account.subscriptionId": "<subscriptionId>",
    "spark.cosmos.account.tenantId": "<tenantId>",
    "spark.cosmos.account.resourceGroupName": "<resourceGroupName>",
    # Throughput control settings
    "spark.cosmos.throughputControl.enabled": "true",
    "spark.cosmos.throughputControl.name": "TargetContainerThroughputControl",
    "spark.cosmos.throughputControl.targetThroughputThreshold": "0.30",
    "spark.cosmos.throughputControl.globalControl.useDedicatedContainer": "false",
}
```
::: zone-end

::: zone pivot="programming-language-scala"

```scala
val cosmosconfig = Map(
  // General settings
  "spark.cosmos.accountEndpoint" -> "<endpoint>",
  "spark.cosmos.database" -> "products",
  "spark.cosmos.container" -> "recommendations",
  // Entra authentication settings
  "spark.cosmos.auth.type" -> "ManagedIdentity",
  "spark.cosmos.account.subscriptionId" -> "<subscriptionId>",
  "spark.cosmos.account.tenantId" -> "<tenantId>",
  "spark.cosmos.account.resourceGroupName" -> "<resourceGroupName>",
  // Throughput control settings
  "spark.cosmos.throughputControl.enabled" -> "true",
  "spark.cosmos.throughputControl.name" -> "TargetContainerThroughputControl",
  "spark.cosmos.throughputControl.targetThroughputThreshold" -> "0.30",
  "spark.cosmos.throughputControl.globalControl.useDedicatedContainer" -> "false"
)
```

::: zone-end

> [!NOTE]
> In this sample, the target database is named `products` and the target container is named `recommendations`.

The throughput configuration, as specified in this step, ensures that only **30%** of the request units (RUs) allocated to the target container are available for Spark operations. 

## Ingest sample product recommendations data to a Delta table

Create a sample DataFrame with product recommendations information for users and write it into a Delta table named `recommendations_delta`. This step simulates curated, transformed data in your data lake that you intend to sync to Azure Cosmos DB for NoSQL. Writing to the Delta format ensures you can later enable change data capture (CDC) for incremental synchronization.

::: zone pivot="programming-language-python"

```python
from pyspark.sql import SparkSession

# Create sample data and convert it to a DataFrame
df = spark.createDataFrame([
    ("yara-lima", "Full-Finger Gloves", "clothing-gloves", 80),
    ("elza-pereira", "Long-Sleeve Logo Jersey", "clothing-jerseys", 90)
], ["id", "productname", "category", "recommendationscore"])

# Write the DataFrame to a Delta table
df.write.mode("append").format("delta").saveAsTable("recommendations_delta")
```

::: zone-end

::: zone pivot="programming-language-scala"

```scala
// Create sample data as a sequence and convert it to a DataFrame
val df = Seq(
  ("yara-lima", "Full-Finger Gloves", "clothing-gloves", 12.95),
  ("elza-pereira", "Long-Sleeve Logo Jersey", "clothing-jerseys", 19.99)
).toDF("id", "productname", "category", "recommendationscore") 

// Write the DataFrame to a table
df.write.mode("append").format("delta").saveAsTable("recommendations_delta")
```

::: zone-end

## Batch load initial data to Azure Cosmos DB for NoSQL

Next, read the `recommendations_delta` Delta table into a Spark DataFrame and perform an initial batch write to Azure Cosmos DB for NoSQL using the `cosmos.oltp` format. Use the **append** mode to add the data without overwriting existing content in the target database and container. This step ensures that all the historic data is available in the account before CDC begins.

::: zone pivot="programming-language-python"

```python
# Read the Delta table into a DataFrame
df_delta = spark.read.format("delta").table("recommendations_delta")

# Write the DataFrame to the container using the Cosmos OLTP format
df_delta.write.format("cosmos.oltp").mode("append").options(**cosmos_config).save()
```

::: zone-end

::: zone pivot="programming-language-scala"

```scala
// Read the Delta table into a DataFrame
val df_delta = spark.read.format("delta").table("recommendations_delta")

// Write the DataFrame to the container using the Cosmos OLTP format
df_delta.write.format("cosmos.oltp").mode("append").options(cosmosconfig).save()
```

::: zone-end

## Enable streaming synchronization with change data feed

Enable Delta Lake's Change Data Feed (CDF) feature on the `recommendations_delta` table by altering the table's properties. CDF allows Delta Lake to track all future row-level inserts, updates, and deletes. Enabling this property is essential for performing incremental syncs to Azure Cosmos DB for NoSQL, as it exposes changes without needing to compare snapshots.

After the historical data load, changes in the Delta table can be captured using Delta Change Data Feed (CDF). You can implement either batch-based or streaming-based CDC.

::: zone pivot="programming-language-python"

### [Batch CDC sync](#tab/batch-cdc-sync)

```python
# Enable Change Data Feed (CDF)
spark.sql("""
  ALTER TABLE recommendations_delta SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")

# Read the Change Data Capture (CDC) data from the Delta table
cdc_batch_df = spark.read.format("delta").option("readChangeData", "true").option("startingVersion", "1").table("recommendations_delta")

# Write the captured changes to Azure Cosmos DB for NoSQL in append mode
cdc_batch_df.write.format("cosmos.oltp").mode("append").options(**cosmos_config).save()
```

### [Stream CDC sync](#tab/stream-cdc-sync)

```python
# Enable Change Data Feed (CDF)
spark.sql("""
  ALTER TABLE recommendations_delta SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")

# Read Change Data Capture (CDC) stream from the Delta table 'recommendations_delta'
cdc_stream_df = spark.readStream.format("delta").option("readChangeData", "true").table("recommendations_delta")

# Write the CDC stream to Azure Cosmos DB for NOSQL using the OLTP connector with checkpointing
streaming_query = cdc_stream_df.writeStream.format("cosmos.oltp").outputMode("append").options(**cosmos_config).option("checkpointLocation", "/mnt/checkpoints/recommendations-stream").start()

# Wait for the stream to terminate or time out after 60 seconds
try:   streaming_query.awaitTermination(60)
except:     print("Stream stopped or timed out.")

# Stop the stream if it’s still running after the timeout
if streaming_query.isActive: streaming_query.stop()
```

---

::: zone-end

::: zone pivot="programming-language-scala"

### [Batch CDC sync](#tab/batch-cdc-sync)

```scala
// Enable Change Data Feed (CDF)
spark.sql("""
  ALTER TABLE recommendations_delta SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")

// Read the Change Data Capture (CDC) data from the Delta table
val cdc_batch_df = spark.read.format("delta").option("readChangeData", "true").option("startingVersion", "1").table("recommendations_delta")

// Write the captured changes to Azure Cosmos DB for NoSQL in append mode
cdc_batch_df.write.format("cosmos.oltp").mode("append").options(cosmos_config).save()
```

### [Stream CDC sync](#tab/stream-cdc-sync)

```scala
// Enable Change Data Feed (CDF)
spark.sql("""
  ALTER TABLE recommendations_delta SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")

// Read Change Data Capture (CDC) stream from the Delta table 'recommendations_delta'
val cdcStreamDF = spark.readStream
  .format("delta")
  .option("readChangeData", "true")
  .table("recommendations_delta")

// Write the CDC stream to Azure Cosmos DB for NoSQL using the OLTP connector with checkpointing
val streamingQuery = cdcStreamDF.writeStream
  .format("cosmos.oltp")
  .outputMode("append")
  .options(cosmosconfig)
  .option("checkpointLocation", "/mnt/checkpoints/recommendations-stream")
  .start()

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

---

::: zone-end

## Verify data using NoSQL queries

After writing to Azure Cosmos DB for NoSQL, verify the data by querying it back into Spark using the same account configuration. Then; inspect the ingested data, run validations, or join with other datasets in Delta Lake for analytics or reporting. Azure Cosmos DB for NoSQL supports fast, indexed reads for real-time query performance.

::: zone pivot="programming-language-python"

```python
# Load DataFrame
df_cosmos = spark.read.format("cosmos.oltp").options(**cosmos_config).load()

# Run query
df_cosmos.select("id", "productname", "category", "recommendationscore").show()
```

::: zone-end

::: zone pivot="programming-language-scala"

```scala
// Load DataFrame
val dfCosmos = spark.read.format("cosmos.oltp").options(cosmosConfig).load()

// Run query
dfCosmos.select("id", "productname", "category", "recommendationscore").show()
```

::: zone-end
    
## Related content

- [Reverse ETL](reverse-extract-transform-load.md)
- [Azure Cosmos DB Spark Connector](/azure/cosmos-db/nosql/tutorial-spark-connector)
- [Microsoft Entra authentication in Apache Spark](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/cosmos/azure-cosmos-spark_3/docs/AAD-Auth.md)
