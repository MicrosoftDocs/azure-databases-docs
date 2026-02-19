---
title: Configure and Use Azure Synapse Link
description: Learn how to enable Synapse Link for Azure Cosmos DB accounts, create a container with analytical store enabled, connect the Azure Cosmos DB database to Synapse workspace, and run queries.
author: jilmal
ms.author: jmaldonado
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 02/19/2026
ms.custom: references_regions, synapse-cosmos-db
appliesto:
  - ✅ NoSQL
---

# Configure and use Azure Synapse Link for Azure Cosmos DB

[!INCLUDE[Note - Synapse Link mirroring support](includes/note-synapse-link-mirroring-support.md)]

[Azure Synapse Link for Azure Cosmos DB](synapse-link.md) is a cloud-native hybrid transactional and analytical processing (HTAP) capability that enables you to run near real-time analytics over operational data in Azure Cosmos DB. Synapse Link creates a tight seamless integration between Azure Cosmos DB and Azure Synapse Analytics.

Azure Synapse Link is available for Azure Cosmos DB SQL API or for Azure Cosmos DB API for Mongo DB accounts. And it is in preview for Gremlin API, with activation via CLI commands. Use the following steps to run analytical queries with the Azure Synapse Link for Azure Cosmos DB:

* [Enable Azure Synapse Link for your Azure Cosmos DB accounts](#enable-synapse-link)
* [Enable Azure Synapse Link for your containers](#update-analytical-ttl)
* [Connect your Azure Cosmos DB database to an Azure Synapse workspace](#connect-to-cosmos-database)
* [Query analytical store using Azure Synapse Analytics](#query)
* [Improve performance with best practices](#synapse-sql-serverless-best-practices-for-azure-synapse-link-for-cosmos-db)

You can also check the training module on how to [configure Azure Synapse Link for Azure Cosmos DB](/training/modules/configure-azure-synapse-link-with-azure-cosmos-db/).

## <a id="enable-synapse-link"></a>Enable Azure Synapse Link for Azure Cosmos DB accounts

The first step to use Synapse Link is to enable it for your Azure Cosmos DB database account.

> [!NOTE]
> If you want to use customer-managed keys with Azure Synapse Link, you must configure your account's managed identity in your Azure Key Vault access policy before enabling Synapse Link on your account. To learn more, see how to [Configure customer-managed keys using Azure Cosmos DB accounts' managed identities](how-to-setup-cmk.md#using-managed-identity) article.

> [!NOTE]
> To configure Full Fidelity Schema for API for NoSQL accounts, enable Synapse Link by using Azure CLI or PowerShell. The selection can't be changed after Synapse Link is enabled. For more information, see [analytical store schema representation documentation](analytical-store-introduction.md#schema-representation).

> [!NOTE]
> You need [Contributor](/azure/role-based-access-control/built-in-roles#databases) role to enable Synapse Link at account level. And you need at least [Operator](/azure/role-based-access-control/built-in-roles#databases) to enable Synapse Link in your containers or collections.

### Command-Line Tools

Enable Synapse Link in your Azure Cosmos DB API for NoSQL or MongoDB account using Azure CLI or PowerShell.

> [!NOTE]
> Turning on Synapse Link does not turn on the analytical store automatically. Once you enable Synapse Link on the Cosmos DB account, enable analytical store on containers to start using Synapse Link. 

#### Azure CLI

Use `--enable-analytical-storage true` for both **create** or **update** operations. You also need to choose the representation schema type. For API for NoSQL accounts you can use `--analytical-storage-schema-type` with the values `FullFidelity` or `WellDefined`. For API for MongoDB accounts, always use `--analytical-storage-schema-type FullFidelity`.

* [Create a new Azure Cosmos DB account with Synapse Link enabled](/cli/azure/cosmosdb#az-cosmosdb-create-optional-parameters)
* [Update an existing Azure Cosmos DB account to enable Synapse Link](/cli/azure/cosmosdb#az-cosmosdb-update-optional-parameters)

##### Use Azure CLI to enable Synapse Link for Azure Synapse Link for Gremlin API account. 
Synapse Link for Gremlin API is now in preview. You can enable Synapse Link in your new or existing graphs using Azure CLI. Use the CLI command below to enable Synapse Link for your Gremlin API account:

```cli
az cosmosdb create --capabilities EnableGremlin --name MyCosmosDBGremlinDatabaseAccount --resource-group MyResourceGroup --enable-analytical-storage true
```

For existing Gremlin API accounts, replace `create` with `update`.

#### PowerShell

Use `EnableAnalyticalStorage true` for both **create** or **update** operations. You also need to choose the representation schema type. For API for NoSQL accounts you can use `--analytical-storage-schema-type` with the values `FullFidelity` or `WellDefined`. For API for MongoDB accounts, always use `-AnalyticalStorageSchemaType FullFidelity`.

* [Create a new Azure Cosmos DB account with Synapse Link enabled](/powershell/module/az.cosmosdb/new-azcosmosdbaccount#description)
* [Update an existing Azure Cosmos DB account to enable Synapse Link](/powershell/module/az.cosmosdb/update-azcosmosdbaccount)

#### Azure Resource Manager template

This [Azure Resource Manager template](./manage-with-templates.md#azure-cosmos-db-account-with-analytical-store) creates a Synapse Link enabled Azure Cosmos DB account for SQL API. This template creates a Core (SQL) API account in one region with a container configured with analytical TTL enabled, and an option to use manual or autoscale throughput. To deploy this template, click on **Deploy to Azure** on the readme page.

## <a id="update-analytical-ttl"></a> Enable Azure Synapse Link for your containers

The second step is to enable Synapse Link for your containers or collections. This is accomplished by setting the `analytical TTL` property to `-1` for infinite retention, or to a positive integer, that is the number of seconds that you want to keep in analytical store. This setting can be changed later. For more information, see the [analytical TTL supported values](analytical-store-introduction.md#analytical-ttl) article.

Please note the following details when enabling Azure Synapse Link on your existing SQL API containers:

* The same performance isolation of the analytical store auto-sync process applies to the initial sync and there is no performance impact on your OLTP workload.
* A container's initial sync with analytical store total time will vary depending on the data volume and on the documents complexity. This process can take anywhere from a few seconds to multiple days.
* The throughput of your container, or database account, also influences the total initial sync time. Although RU/s are not used in this migration, the total RU/s available influences the performance of the process. You can temporarily increase your environment's available RUs to speed up the process.
* You won't be able to query analytical store of an existing container while Synapse Link is being enabled on that container. Your OLTP workload isn't impacted and you can keep on reading data normally. Data ingested after the start of the initial sync will be merged into analytical store by the regular analytical store auto-sync process.

> [!NOTE]
> Now you can enable Synapse Link on your existing MongoDB API collections, using Azure CLI or PowerShell.

### Command-Line Tools

#### Azure CLI

The following options enable Synapse Link in a container by using Azure CLI by setting the `--analytical-storage-ttl` property. 

* [Create or update an Azure Cosmos DB MongoDB collection](/cli/azure/cosmosdb/mongodb/collection#az-cosmosdb-mongodb-collection-create-examples)
* [Create or update an Azure Cosmos DB SQL API container](/cli/azure/cosmosdb/sql/container#az-cosmosdb-sql-container-create)

##### Use Azure CLI to enable Synapse Link for Azure Synapse Link for Gremlin API Graphs

Synapse Link for Gremlin API is now in preview. You can enable Synapse Link in your new or existing Graphs using Azure CLI. Use the CLI command below to enable Synapse Link for your Gremlin API graphs:

```cli
az cosmosdb gremlin graph create --g MyResourceGroup --a MyCosmosDBGremlinDatabaseAccount --d MyGremlinDB --n MyGraph --analytical-storage-ttl –1
```

For existing graphs, replace `create` with `update`.

#### PowerShell

The following options enable Synapse Link in a container by using Azure CLI by setting the `-AnalyticalStorageTtl` property. 

* [Create or update an Azure Cosmos DB MongoDB collection](/powershell/module/az.cosmosdb/new-azcosmosdbmongodbcollection#description)
* [Create or update an Azure Cosmos DB SQL API container](/powershell/module/az.cosmosdb/new-azcosmosdbsqlcontainer)


### Azure Cosmos DB SDKs - SQL API only

#### .NET SDK

The following .NET code creates a Synapse Link enabled container by setting the `AnalyticalStoreTimeToLiveInSeconds` property. To update an existing container, use the `Container.ReplaceContainerAsync` method.

```csharp
CosmosClient cosmosClient = new CosmosClient(
    accountEndpoint: "<nosql-account-endpoint>",
    tokenCredential: new DefaultAzureCredential()
);
```

```csharp
// Create a container with a partition key, and analytical TTL configured to -1 (infinite retention)
ContainerProperties properties = new ContainerProperties()
{
    Id = "myContainerId",
    PartitionKeyPath = "/id",
    AnalyticalStoreTimeToLiveInSeconds = -1,
};
await cosmosClient.GetDatabase("myDatabase").CreateContainerAsync(properties);
```

#### Java V4 SDK

The following Java code creates a Synapse Link enabled container by setting the `setAnalyticalStoreTimeToLiveInSeconds` property. To update an existing container, use the `container.replace` class.

```java
// Create a container with a partition key and  analytical TTL configured to  -1 (infinite retention) 
CosmosContainerProperties containerProperties = new CosmosContainerProperties("myContainer", "/myPartitionKey");

containerProperties.setAnalyticalStoreTimeToLiveInSeconds(-1);

container = database.createContainerIfNotExists(containerProperties, 400).block().getContainer();
```

#### Python V4 SDK

The following Python code creates a Synapse Link enabled container by setting the `analytical_storage_ttl` property. To update an existing container, use the `replace_container` method.

```python
# Client

client = cosmos_client.CosmosClient(HOST,  KEY )

# Database client
try:
    db = client.create_database(DATABASE)

except exceptions.CosmosResourceExistsError:
    db = client.get_database_client(DATABASE)

# Creating the container with analytical store enabled
try:
    container = db.create_container(
        id=CONTAINER,
        partition_key=PartitionKey(path='/id', kind='Hash'),analytical_storage_ttl=-1
    )
    properties = container.read()
    print('Container with id \'{0}\' created'.format(container.id))
    print('Partition Key - \'{0}\''.format(properties['partitionKey']))

except exceptions.CosmosResourceExistsError:
    print('A container with already exists')
```

## <a id="connect-to-cosmos-database"></a> Connect to a Synapse workspace

Use the instructions in [Connect to Azure Synapse Link](/azure/synapse-analytics/synapse-link/how-to-connect-synapse-link-cosmos-db) on how to access an Azure Cosmos DB database from Azure Synapse Analytics Studio with Azure Synapse Link.

## <a id="query"></a> Query analytical store using Azure Synapse Analytics

### Query analytical store using Apache Spark for Azure Synapse Analytics

Use the instructions in the [Query Azure Cosmos DB analytical store using Spark 3](/azure/synapse-analytics/synapse-link/how-to-query-analytical-store-spark-3) article on how to query with Synapse Spark 3. That article gives some examples on how you can interact with the analytical store from Synapse gestures. Those gestures are visible when you right-click on a container. With gestures, you can quickly generate code and tweak it to your needs. They are also perfect for discovering data with a single click.

For Spark 2 integration use the instruction in the [Query Azure Cosmos DB analytical store using Spark 2](/azure/synapse-analytics/synapse-link/how-to-query-analytical-store-spark) article.

### Custom Partitioning

Custom partitioning enables you to partition analytical store data on fields that are commonly used as filters in analytical queries, resulting in improved query performance. To learn more, see the [introduction to custom partitioning](custom-partitioning-analytical-store.md) and [how to configure custom partitioning](configure-custom-partitioning.md) articles.

### Synapse SQL Serverless best practices for Azure Synapse Link for Cosmos DB

Use [this](https://techcommunity.microsoft.com/t5/azure-synapse-analytics-blog/best-practices-for-integrating-serverless-sql-pool-with-cosmos/ba-p/3257975) mandatory best practices for your SQL serverless queries.


## <a id="cosmosdb-synapse-link-samples"></a> Getting started with Azure Synapse Link - Samples

You can find samples to get started with Azure Synapse Link on [GitHub](https://aka.ms/cosmosdb-synapselink-samples). These showcase end-to-end solutions with IoT and retail scenarios. You can also find the samples corresponding to Azure Cosmos DB for MongoDB in the same repo under the [MongoDB](https://github.com/Azure-Samples/Synapse/tree/main/Notebooks/PySpark/Synapse%20Link%20for%20Cosmos%20DB%20samples) folder. 

## Next steps

To learn more, see the following docs:

* Check the training module on how to [configure Azure Synapse Link for Azure Cosmos DB.](/training/modules/configure-azure-synapse-link-with-azure-cosmos-db/)
* [Azure Cosmos DB analytical store overview.](analytical-store-introduction.md)
* [Frequently asked questions about Synapse Link for Azure Cosmos DB.](synapse-link-frequently-asked-questions.yml)
* [Apache Spark in Azure Synapse Analytics](/azure/synapse-analytics/spark/apache-spark-concepts).
* [Serverless SQL pool runtime support in Azure Synapse Analytics](/azure/synapse-analytics/sql/on-demand-workspace-overview).
