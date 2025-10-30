---
title: 'Migrate Your Data to an API for Cassandra Account in Azure Cosmos DB - Tutorial'
description: In this tutorial, learn how to copy data from Apache Cassandra to an API for Cassandra account in Azure Cosmos DB.
author: TheovanKraay
ms.author: thvankra
ms.service: azure-cosmos-db
ms.subservice: apache-cassandra
ms.topic: tutorial
ms.date: 06/09/2025
ms.devlang: csharp
#Customer intent: As a developer, I want to migrate my existing Cassandra workloads to Azure Cosmos DB so that the overhead to manage resources, clusters, and garbage collection is automatically handled by Azure Cosmos DB.
---

# Tutorial: Migrate your data to an API for Cassandra account
[!INCLUDE[Cassandra](../includes/appliesto-cassandra.md)]

As a developer, you might have existing Cassandra workloads that are running on-premises or in the cloud. You might want to migrate them to Azure. You can migrate such workloads to an API for Cassandra account in Azure Cosmos DB. This tutorial provides instructions on different options that are available to migrate Apache Cassandra data into the API for Cassandra account in Azure Cosmos DB.

This tutorial covers the following tasks:

> [!div class="checklist"]
> - Plan for migration.
> - Meet prerequisites for migration.
> - Migrate data by using the `cqlsh` `COPY` command.
> - Migrate data by using Spark.

If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Prerequisites for migration

- **Estimate your throughput needs:** Before you migrate data to the API for Cassandra account in Azure Cosmos DB, estimate the throughput needs of your workload. In general, start with the average throughput required by the create, read, update, and delete (CRUD) operations. Then include the extra throughput required for the extract, transform, and load (ETL) or spiky operations. You need the following details to plan for migration:

  - **Existing data size or estimated data size:** Defines the minimum database size and throughput requirement. If you estimate data size for a new application, you can assume that the data is uniformly distributed across the rows. You can estimate the value by multiplying with the data size.
  - **Required throughput:** Approximate throughput rate of read (query/get) and write (update/delete/insert) operations. This value is required to compute the required request units, along with steady-state data size.
  - **The schema:** Connect to your existing Cassandra cluster through `cqlsh`, and export the schema from Cassandra:

    ```bash
    cqlsh [IP] "-e DESC SCHEMA" > orig_schema.cql
    ```

    After you identify the requirements of your existing workload, create an Azure Cosmos DB account, database, and containers according to the gathered throughput requirements.

  - **Determine the request unit (RU) charge for an operation:** You can determine the RUs by using any of the SDKs supported by the API for Cassandra. This example shows the .NET version of getting RU charges.

    ```csharp
    var tableInsertStatement = table.Insert(sampleEntity);
    var insertResult = await tableInsertStatement.ExecuteAsync();

    foreach (string key in insertResult.Info.IncomingPayload)
      {
         byte[] valueInBytes = customPayload[key];
         double value = Encoding.UTF8.GetString(valueInBytes);
         Console.WriteLine($"CustomPayload:  {key}: {value}");
      }
    ```

- **Allocate the required throughput:** Azure Cosmos DB can automatically scale storage and throughput as your requirements grow. You can estimate your throughput needs by using the [Azure Cosmos DB RU calculator](https://cosmos.azure.com/capacitycalculator).
- **Create tables in the API for Cassandra account:** Before you start migrating data, precreate all of your tables from the Azure portal or from `cqlsh`. If you're migrating to an Azure Cosmos DB account that has database-level throughput, provide a partition key when you create the containers.
- **Increase throughput:** The duration of your data migration depends on the amount of throughput you provisioned for the tables in Azure Cosmos DB. Increase the throughput during migration. With higher throughput, you can avoid rate limiting and migrate in less time. After you finish the migration, decrease the throughput to save costs. We also recommend that you have the Azure Cosmos DB account in the same region as your source database.
- **Enable Transport Layer Security (TLS):** Azure Cosmos DB has strict security requirements and standards. Enable TLS when you interact with your account. When you use the Cassandra Query Language (CQL) with Secure Shell, you can provide TLS information.

## Options to migrate data

You can move data from existing Cassandra workloads to Azure Cosmos DB by using the `cqlsh` `COPY` command or by using Spark.

### Migrate data by using the cqlsh COPY command

> [!WARNING]
> Only use the CQL `COPY` command to migrate small datasets. To move large datasets, [migrate data by using Spark](#migrate-data-by-using-spark).

1. To be certain that your .csv file contains the correct file structure, use the `COPY TO` command to export data directly from your source Cassandra table to a .csv file. Ensure that `cqlsh` is connected to the source table by using the appropriate credentials.

   ```bash
   COPY exampleks.tablename TO 'data.csv' WITH HEADER = TRUE;   
   ```

1. Now get your API for Cassandra account's connection string information:

   1. Sign in to the [Azure portal](https://portal.azure.com), and go to your Azure Cosmos DB account.
   1. Open the **Connection String** pane. Here you see all the information that you need to connect to your API for Cassandra account from `cqlsh`.

1. Sign in to `cqlsh` by using the connection information from the Azure portal.

1. Use the CQL `COPY FROM` command to copy `data.csv`. This file is still located in the user root directory where `cqlsh` is installed.

   ```bash
   COPY exampleks.tablename FROM 'data.csv' WITH HEADER = TRUE;
   ```

> [!NOTE]
> The API for Cassandra supports protocol version 4, which shipped with Cassandra 3.11. There might be issues if you use later protocol versions with our API. With a later protocol version, the `COPY FROM` command can go into a loop and return duplicate rows.
>
> Add `protocol-version` to the `cqlsh` command:
>
> ```sql
> cqlsh <USERNAME>.cassandra.cosmos.azure.com 10350 -u <USERNAME> -p <PASSWORD> --ssl --protocol-version=4
> ```

#### Add throughput-limiting options to the CQL COPY command

The `COPY` command in `cqlsh` supports various parameters to control the rate of ingestion of documents into Azure Cosmos DB.

The default configuration for the `COPY` command tries to ingest data at a fast pace. It doesn't account for the rate-limiting behavior of Azure Cosmos DB. Reduce `CHUNKSIZE` or `INGESTRATE` depending on the throughput configured on the collection.

We recommend the following configuration (at a minimum) for a collection at 20,000 RUs if the document or record size is 1 KB:

- `CHUNKSIZE` = 100
- `INGESTRATE` = 500
- `MAXATTEMPTS` = 10

##### Example commands

- Copy data from the API for Cassandra to a local .csv file:

  ```sql
  COPY standard1 (key, "C0", "C1", "C2", "C3", "C4") TO 'backup.csv' WITH PAGESIZE=100 AND MAXREQUESTS=1 ;
  ```

- Copy data from a local .csv file to the API for Cassandra:

  ```sql
  COPY standard2 (key, "C0", "C1", "C2", "C3", "C4") FROM 'backup.csv' WITH CHUNKSIZE=100 AND INGESTRATE=100 AND MAXATTEMPTS=10;
  ```

>[!IMPORTANT]
> Only the open-source Apache Cassandra version of `CQLSH COPY` is supported. Datastax Enterprise (DSE) versions of `CQLSH` might encounter errors.

### Migrate data by using Spark

To migrate data to the API for Cassandra account with Spark, follow these steps:

1. Provision an [Azure Databricks cluster](spark-databricks.md) or an [Azure HDInsight cluster](spark-hdinsight.md).

1. Move data to the destination API for Cassandra endpoint. For more information, see [Migrate data from Cassandra to an Azure Cosmos DB for Apache Cassandra account](migrate-data-databricks.md).

  If you have data that resides in an existing cluster in Azure virtual machines or any other cloud, we recommend that you use Spark jobs to migrate the data. Set up Spark as an intermediary for one-time or regular ingestion. You can accelerate this migration by using Azure ExpressRoute connectivity between your on-premises environment and Azure.

### Live migration

If you need a zero-downtime migration from a native Apache Cassandra cluster, we recommend that you configure dual-writes and a separate bulk data load to migrate historical data. Implementing this pattern is more straightforward when you use an open-source [dual-write proxy](https://github.com/Azure-Samples/cassandra-proxy) to allow for minimal application code changes. For more information, see [Live migrate data from Apache Cassandra to the Azure Cosmos DB for Apache Cassandra](migrate-data-dual-write-proxy.md).

## Clean up resources

When resources are no longer needed, you can delete the resource group, the Azure Cosmos DB account, and all the related resources. To do so, select the resource group for the virtual machine, select **Delete**, and then confirm the name of the resource group to delete.

## Next step

In this tutorial, you learned how to migrate your data to an API for Cassandra account in Azure Cosmos DB. You can now learn about other concepts in Azure Cosmos DB:

> [!div class="nextstepaction"]
> [Tunable data consistency levels in Azure Cosmos DB](../consistency-levels.md)
