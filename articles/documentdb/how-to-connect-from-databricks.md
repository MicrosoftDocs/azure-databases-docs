---
title: Connect from Azure Databricks
description: Learn how to connect to Azure DocumentDB from Azure Databricks using Python and Spark. Perform read, write, filter, and aggregation operations. Start building today.
author: niklarin
ms.author: nlarin
ms.topic: how-to
ms.date: 11/05/2025
ms.custom:
  - devx-track-python
  - sfi-ropc-blocked
ai-usage: ai-generated
#customer intent: As a data engineer, I want to connect to Azure DocumentDB from Azure Databricks so that I can perform data operations using Python and Spark.
---

# Connect to Azure DocumentDB from Azure Databricks

This article shows you how to connect to Azure DocumentDB from Azure Databricks to perform common data operations using Python and Spark. You configure the necessary dependencies, establish a connection, and execute read, write, filter, and aggregation operations with the MongoDB Spark connector.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]
  
  - [Firewall configured to allow access from Azure services](how-to-configure-firewall.md#grant-access-from-azure-services)

- Spark environment in [Azure Databricks](/azure/databricks/scenarios/quickstart-create-databricks-workspace-portal)

  - MongoDB Spark connector compatible with Spark 3.2.1 or higher (available at Maven coordinates `org.mongodb.spark:mongo-spark-connector_2.12:3.0.1`)

## Configure Azure Databricks workspace

Configure your Azure Databricks workspace to connect to Azure DocumentDB. Add the MongoDB Connector for Spark library to your compute to enable connectivity to Azure DocumentDB.

1. Navigate to your Azure Databricks workspace.

1. Configure the default compute available or [create a new compute resource](/azure/databricks/compute/configure#create-a-new-all-purpose-compute-resource) to run your notebook.

1. Select a Databricks runtime that supports at least Spark 3.0.

1. In your compute resource, select **Libraries** > **Install New** > **Maven**.

1. Add the Maven coordinates: `org.mongodb.spark:mongo-spark-connector_2.12:3.0.1`

1. Select **Install**.

1. Restart the compute when installation is complete.

## Configure connection settings

Configure Spark to use your Azure DocumentDB connection string for all read and write operations.

1. In the Azure portal, navigate to your Azure DocumentDB resource.

1. Under **Settings** > **Connection strings**, copy the connection string. It has the form: `mongodb+srv://<user>:<password>@<database_name>.mongocluster.cosmos.azure.com`

1. In Azure Databricks, navigate to your compute configuration and select **Advanced Options** (at the bottom of the page).

1. Add the following Spark configuration variables:
   - `spark.mongodb.output.uri` - Paste your connection string
   - `spark.mongodb.input.uri` - Paste your connection string

1. Save the configuration.

Alternatively, you can set the connection string directly in your code by using the `.option()` method when reading or writing data.

## Create Python notebook

Run your data operations by creating a new Python notebook.

1. In your Azure Databricks workspace, create a new Python notebook.

1. Define your connection variables at the beginning of the notebook:

   ```python
   connectionString = "mongodb+srv://<user>:<password>@<database_name>.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
   database = "<database_name>"
   collection = "<collection_name>"
   ```

1. Replace the placeholder values with your actual database name and collection name.

## Read data from collection

Read data from your Azure DocumentDB collection into a Spark DataFrame.

1. Use the following code to load data from your collection:

   ```python
   df = spark.read.format("mongo").option("database", database).option("spark.mongodb.input.uri", connectionString).option("collection", collection).load()
   ```

1. Verify the data loaded successfully:

   ```python
   df.printSchema()
   display(df)
   ```

1. Observe the result. This code creates a DataFrame containing all documents from the specified collection and displays the schema and data.

## Filter data

Apply filters to retrieve specific subsets of data from your collection.

1. Use the DataFrame `filter()` method to apply conditions:

   ```python
   df_filtered = df.filter(df["birth_year"] == 1970)
   display(df_filtered)
   ```

1. Use column index numbers:

   ```python
   df_filtered = df.filter(df[2] == 1970)
   display(df_filtered)
   ```

1. Observe the result. This approach returns only the documents that match your filter criteria.

## Query data with SQL

Create temporary views and run SQL queries against your data for familiar SQL-based analysis.

1. Create a temporary view from your DataFrame:

   ```python
   df.createOrReplaceTempView("T")
   ```

1. Execute SQL queries against the view:

   ```python
   df_result = spark.sql("SELECT * FROM T WHERE birth_year == 1970 AND gender == 2")
   display(df_result)
   ```

1. Observe the result. This approach allows you to use standard SQL syntax for complex queries and joins.

## Write data to collection

Save new or modified data by writing DataFrames back to Azure DocumentDB collections.

1. Use the following code to write data to a collection:

   ```python
   df.write.format("mongo").option("spark.mongodb.output.uri", connectionString).option("database", database).option("collection", "CitiBike2019").mode("append").save()
   ```

1. The write operation completes without output. Verify that the write operation completed successfully by reading the data from the collection:

   ```python
   df_verify = spark.read.format("mongo").option("database", database).option("spark.mongodb.input.uri", connectionString).option("collection", "CitiBike2019").load()
   display(df_verify)
   ```

    > [!TIP]
    > Use different write modes such as `append`, `overwrite`, or `ignore` depending on your requirements.

## Run aggregation pipelines

Execute aggregation pipelines to perform server-side data processing and analytics directly within Azure DocumentDB. Aggregation pipelines enable powerful data transformations, grouping, and calculations without moving data out of the database. They're ideal for real-time analytics, dashboards, and report generation.

1. Define your aggregation pipeline as a JSON string:

   ```python
   pipeline = "[{ $group : { _id : '$birth_year', totaldocs : { $count : 1 }, totalduration: {$sum: '$tripduration'}} }]"
   ```

1. Execute the pipeline and load the results:

   ```python
   df_aggregated = spark.read.format("mongo").option("database", database).option("spark.mongodb.input.uri", connectionString).option("collection", collection).option("pipeline", pipeline).load()
   display(df_aggregated)
   ```

## Related content

- [Maven central](https://mvnrepository.com/artifact/org.mongodb.spark/mongo-spark-connector) - MongoDB Spark connector versions
- [Practical MongoDB Aggregations](https://www.practical-mongodb-aggregations.com/front-cover.html) - Guide to aggregation pipelines
- [Configure firewall settings](how-to-configure-firewall.md)
