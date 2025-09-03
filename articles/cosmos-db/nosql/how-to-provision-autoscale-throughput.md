---
title: Provision Autoscale Throughput
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to provision autoscale throughput at the container and database level in Azure Cosmos DB for NoSQL using Azure portal, CLI, PowerShell, and various other SDKs. 
author: deborahc
ms.author: dech
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 09/03/2025
ms.custom: devx-track-csharp, devx-track-azurecli, devx-track-azurepowershell, devx-track-arm-template, devx-track-dotnet, devx-track-extended-java
applies-to:
  - NoSQL
---

# Provision autoscale throughput for Azure Cosmos DB for NoSQL

This article explains how to enable autoscale throughput on a database or container (collection, graph, or table) in Azure Cosmos DB for NoSQL. You can enable autoscale on a single container, or provision autoscale throughput on a database and share it among all the containers in the database.

If you're using a different API, see [API for MongoDB](../mongodb/how-to-provision-throughput.md), [API for Cassandra](../cassandra/how-to-provision-throughput.md), or [API for Gremlin](../gremlin/how-to-provision-throughput.md).

## Azure portal

### Create new database or container with autoscale

1. Sign in to the [Azure portal](https://portal.azure.com) or the [Azure Cosmos DB explorer](https://cosmos.azure.com).

1. Navigate to your Azure Cosmos DB account and open the **Data Explorer** tab.

1. Select **New Container.** Enter a name for your database, container, and a partition key.

1. Under database or container throughput, select the **Autoscale** option, and set the [maximum throughput (RU/s)](../provision-throughput-autoscale.md) that you want the database or container to scale to.

   :::image type="content" source="./media/how-to-provision-autoscale-throughput/create-new-autoscale-container.png" alt-text="Screenshot that shows the settings to create a container and configure autoscale provisioned throughput." lightbox="./media/how-to-provision-autoscale-throughput/create-new-autoscale-container.png":::

1. Select **OK**.

To provision autoscale on shared throughput database, select the **Provision database throughput** option when creating a new database. 

### Enable autoscale on existing database or container

1. Sign in to the [Azure portal](https://portal.azure.com) or the [Azure Cosmos DB explorer](https://cosmos.azure.com).

1. Navigate to your Azure Cosmos DB account and open the **Data Explorer** tab.

1. Select **Scale and Settings** for your container, or **Scale** for your database.

1. Under **Scale**, select the **Autoscale** option and **Save**.

   :::image type="content" source="./media/how-to-provision-autoscale-throughput/autoscale-scale-and-settings.png" alt-text="Screenshot of settings to enable autoscale on an existing container.":::

> [!NOTE]
> When you enable autoscale on an existing database or container, the starting value for max RU/s is determined by the system, based on your current manual provisioned throughput settings and storage. After the operation completes, you can change the max RU/s if needed. To learn more, see [Frequently asked questions about autoscale provisioned throughput](../autoscale-faq.yml#how-does-the-migration-between-autoscale-and-standard--manual--provisioned-throughput-work-).

## Azure Cosmos DB .NET V3 SDK

Use [version 3.9 or higher](https://www.nuget.org/packages/Microsoft.Azure.Cosmos) of the Azure Cosmos DB .NET SDK for API for NoSQL to manage autoscale resources. 

> [!IMPORTANT]
> You can use the .NET SDK to create new autoscale resources. The SDK doesn't support migrating between autoscale and standard (manual) throughput. The migration scenario is currently supported in only the [Azure portal](#enable-autoscale-on-existing-database-or-container), [CLI](#azure-cli), and [PowerShell](#azure-powershell).

### Create database with shared throughput

```csharp
// Create instance of CosmosClient
CosmosClient cosmosClient = new CosmosClient(Endpoint, PrimaryKey);
 
// Autoscale throughput settings
ThroughputProperties autoscaleThroughputProperties = ThroughputProperties.CreateAutoscaleThroughput(1000); //Set autoscale max RU/s

//Create the database with autoscale enabled
database = await cosmosClient.CreateDatabaseAsync(DatabaseName, throughputProperties: autoscaleThroughputProperties);
```

### Create container with dedicated throughput

```csharp
// Get reference to database that container will be created in
Database database = await cosmosClient.GetDatabase("DatabaseName");

// Container and autoscale throughput settings
ContainerProperties autoscaleContainerProperties = new ContainerProperties("ContainerName", "/partitionKey");
ThroughputProperties autoscaleThroughputProperties = ThroughputProperties.CreateAutoscaleThroughput(1000); //Set autoscale max RU/s

// Create the container with autoscale enabled
container = await database.CreateContainerAsync(autoscaleContainerProperties, autoscaleThroughputProperties);
```

### Read the current throughput (RU/s)

```csharp
// Get a reference to the resource
Container container = cosmosClient.GetDatabase("DatabaseName").GetContainer("ContainerName");

// Read the throughput on a resource
ThroughputProperties autoscaleContainerThroughput = await container.ReadThroughputAsync(requestOptions: null); 

// The autoscale max throughput (RU/s) of the resource
int? autoscaleMaxThroughput = autoscaleContainerThroughput.AutoscaleMaxThroughput;

// The throughput (RU/s) the resource is currently scaled to
int? currentThroughput = autoscaleContainerThroughput.Throughput;
```

### Change the autoscale max throughput (RU/s)

```csharp
// Change the autoscale max throughput (RU/s)
await container.ReplaceThroughputAsync(ThroughputProperties.CreateAutoscaleThroughput(newAutoscaleMaxThroughput));
```

## Azure Cosmos DB Java V4 SDK

You can use [version 4.0 or higher](https://mvnrepository.com/artifact/com.azure/azure-cosmos) of the Azure Cosmos DB Java SDK for API for NoSQL to manage autoscale resources.

> [!IMPORTANT]
> You can use the Java SDK to create new autoscale resources. The SDK doesn't support migrating between autoscale and standard (manual) throughput. The migration scenario is currently supported in only the [Azure portal](#enable-autoscale-on-existing-database-or-container), [CLI](#azure-cli), and [PowerShell](#azure-powershell).

### Create database with shared throughput

# [Async](#tab/api-async)

```java
// Create instance of CosmosClient
CosmosAsyncClient client = new CosmosClientBuilder()
    .setEndpoint(HOST)
    .setKey(PRIMARYKEY)
    .setConnectionPolicy(CONNECTIONPOLICY)
    .buildAsyncClient();

// Autoscale throughput settings
ThroughputProperties autoscaleThroughputProperties = ThroughputProperties.createAutoscaledThroughput(1000); //Set autoscale max RU/s

//Create the database with autoscale enabled
CosmosAsyncDatabase database = client.createDatabase(databaseName, autoscaleThroughputProperties).block().getDatabase();
```

# [Sync](#tab/api-sync)

```java
// Create instance of CosmosClient
CosmosClient client = new CosmosClientBuilder()
    .setEndpoint(HOST)
    .setKey(PRIMARYKEY)
    .setConnectionPolicy(CONNECTIONPOLICY)
    .buildClient();

// Autoscale throughput settings
ThroughputProperties autoscaleThroughputProperties = ThroughputProperties.createAutoscaledThroughput(1000); //Set autoscale max RU/s

//Create the database with autoscale enabled
CosmosDatabase database = client.createDatabase(databaseName, autoscaleThroughputProperties).getDatabase();
```

--- 

### Create container with dedicated throughput

# [Async](#tab/api-async)

```java
// Get reference to database that container will be created in
CosmosAsyncDatabase database = client.createDatabase("DatabaseName").block().getDatabase();

// Container and autoscale throughput settings
CosmosContainerProperties autoscaleContainerProperties = new CosmosContainerProperties("ContainerName", "/partitionKey");
ThroughputProperties autoscaleThroughputProperties = ThroughputProperties.createAutoscaledThroughput(1000); //Set autoscale max RU/s

// Create the container with autoscale enabled
CosmosAsyncContainer container = database.createContainer(autoscaleContainerProperties, autoscaleThroughputProperties, new CosmosContainerRequestOptions())
                                .block()
                                .getContainer();
```

# [Sync](#tab/api-sync)

```java
// Get reference to database that container will be created in
CosmosDatabase database = client.createDatabase("DatabaseName").getDatabase();

// Container and autoscale throughput settings
CosmosContainerProperties autoscaleContainerProperties = new CosmosContainerProperties("ContainerName", "/partitionKey");
ThroughputProperties autoscaleThroughputProperties = ThroughputProperties.createAutoscaledThroughput(1000); //Set autoscale max RU/s

// Create the container with autoscale enabled
CosmosContainer container = database.createContainer(autoscaleContainerProperties, autoscaleThroughputProperties, new CosmosContainerRequestOptions())
                                .getContainer();
```

--- 

### Read the current throughput (RU/s)

# [Async](#tab/api-async)

```java
// Get a reference to the resource
CosmosAsyncContainer container = client.getDatabase("DatabaseName").getContainer("ContainerName");

// Read the throughput on a resource
ThroughputProperties autoscaleContainerThroughput = container.readThroughput().block().getProperties();

// The autoscale max throughput (RU/s) of the resource
int autoscaleMaxThroughput = autoscaleContainerThroughput.getAutoscaleMaxThroughput();

// The throughput (RU/s) the resource is currently scaled to
int currentThroughput = autoscaleContainerThroughput.Throughput;
```

# [Sync](#tab/api-sync)

```java
// Get a reference to the resource
CosmosContainer container = client.getDatabase("DatabaseName").getContainer("ContainerName");

// Read the throughput on a resource
ThroughputProperties autoscaleContainerThroughput = container.readThroughput().getProperties();

// The autoscale max throughput (RU/s) of the resource
int autoscaleMaxThroughput = autoscaleContainerThroughput.getAutoscaleMaxThroughput();

// The throughput (RU/s) the resource is currently scaled to
int currentThroughput = autoscaleContainerThroughput.Throughput;
```

--- 

### Change the autoscale max throughput (RU/s)

# [Async](#tab/api-async)

```java
// Change the autoscale max throughput (RU/s)
container.replaceThroughput(ThroughputProperties.createAutoscaledThroughput(newAutoscaleMaxThroughput)).block();
```

# [Sync](#tab/api-sync)

```java
// Change the autoscale max throughput (RU/s)
container.replaceThroughput(ThroughputProperties.createAutoscaledThroughput(newAutoscaleMaxThroughput));
```

---

## Azure Cosmos DB Go SDK

You can use [ThroughputProperties](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos#ThroughputProperties) on database and container resources.

### Create a database with manual throughput

```go
// manual throughput properties
db_throughput := azcosmos.NewManualThroughputProperties(400)

_, err = client.CreateDatabase(context.Background(), azcosmos.DatabaseProperties{
	ID: "demo_db",
}, &azcosmos.CreateDatabaseOptions{
	ThroughputProperties: &db_throughput,
})
```

### Create a container with autoscale throughput

```go
pkDefinition := azcosmos.PartitionKeyDefinition{
	Paths: []string{"/state"},
	Kind:  azcosmos.PartitionKeyKindHash,
}

// autoscale throughput properties
throughput := azcosmos.NewAutoscaleThroughputProperties(4000)

db.CreateContainer(context.Background(), azcosmos.ContainerProperties{
	ID:                     "demo_container",
	PartitionKeyDefinition: pkDefinition,
}, &azcosmos.CreateContainerOptions{
	ThroughputProperties: &throughput,
})
```

---

## Azure Resource Manager

Azure Resource Manager templates can be used to provision autoscale throughput on a new database or container-level resource for all Azure Cosmos DB APIs. For samples, see [Azure Resource Manager templates for Azure Cosmos DB](./samples-resource-manager-templates.md).

By design, Azure Resource Manager templates can't be used to migrate between provisioned and autoscale throughput on an existing resource. 

## Azure CLI

Azure CLI can be used to provision autoscale throughput on a new database or container-level resource for all Azure Cosmos DB APIs, or to enable autoscale on an existing resource.

## Azure PowerShell

Azure PowerShell can be used to provision autoscale throughput on a new database or container-level resource for all Azure Cosmos DB APIs, or to enable autoscale on an existing resource.

## Next steps

* [Benefits of provisioned throughput with autoscale](../provision-throughput-autoscale.md#benefits-of-autoscale)
* [How to choose between standard (manual) and autoscale provisioned throughput](../how-to-choose-offer.md)
* [Frequently asked questions about autoscale provisioned throughput in Azure Cosmos DB](../autoscale-faq.yml)
