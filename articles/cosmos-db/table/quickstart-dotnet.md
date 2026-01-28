---
title: Quickstart - Azure SDK for .NET
titleSuffix: Azure Cosmos DB for Table
description: Deploy a .NET web application that uses the Azure SDK for .NET to interact with Azure Cosmos DB for Table data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: table
ms.devlang: csharp
ms.topic: quickstart-sdk
ms.date: 04/08/2025
ms.custom: devx-track-csharp, devx-track-dotnet, devx-track-extended-azdevcli
# CustomerIntent: As a developer, I want to learn the basics of the .NET library so that I can build applications with Azure Cosmos DB for Table.
---

# Quickstart: Use Azure Cosmos DB for Table with Azure SDK for .NET

[!INCLUDE[Developer Quickstart selector](includes/quickstart/dev-selector.md)]

In this quickstart, you deploy a basic Azure Cosmos DB for Table application using the Azure SDK for .NET. Azure Cosmos DB for Table is a schemaless data store allowing applications to store structured table data in the cloud. You learn how to create tables, rows, and perform basic tasks within your Azure Cosmos DB resource using the Azure SDK for .NET.

[API reference documentation](/dotnet/api/azure.data.tables) | [Library source code](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/tables/Azure.Data.Tables) | [Package (NuGet)](https://www.nuget.org/packages/Azure.Data.Tables/) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

- Azure Developer CLI
- Docker Desktop
- .NET 9.0

If you don't have an Azure account, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Initialize the project

Use the Azure Developer CLI (`azd`) to create an Azure Cosmos DB for Table account and deploy a containerized sample application. The sample application uses the client library to manage, create, read, and query sample data.

1. Open a terminal in an empty directory.

1. If you're not already authenticated, authenticate to the Azure Developer CLI using `azd auth login`. Follow the steps specified by the tool to authenticate to the CLI using your preferred Azure credentials.

    ```azurecli
    azd auth login
    ```

1. Use `azd init` to initialize the project.

    ```azurecli
    azd init --template cosmos-db-table-dotnet-quickstart
    ```

1. During initialization, configure a unique environment name.

1. Deploy the Azure Cosmos DB account using `azd up`. The Bicep templates also deploy a sample web application.

    ```azurecli
    azd up
    ```

1. During the provisioning process, select your subscription, desired location, and target resource group. Wait for the provisioning process to complete. The process can take **approximately five minutes**.

1. Once the provisioning of your Azure resources is done, a URL to the running web application is included in the output.

    ```output
    Deploying services (azd deploy)
    
      (✓) Done: Deploying service web
    - Endpoint: <https://[container-app-sub-domain].azurecontainerapps.io>
    
    SUCCESS: Your application was provisioned and deployed to Azure in 5 minutes 0 seconds.
    ```

1. Use the URL in the console to navigate to your web application in the browser. Observe the output of the running app.

:::image type="content" source="media/quickstart-dotnet/running-application.png" alt-text="Screenshot of the running web application.":::

### Install the client library

The client library is available through NuGet, as the `Azure.Data.Tables` package.

1. Open a terminal and navigate to the `/src/web` folder.

    ```bash
    cd ./src/web
    ```

1. If not already installed, install the `Azure.Data.Tables` package using `dotnet add package`.

    ```bash
    dotnet add package Azure.Data.Tables
    ```

1. Open and review the **src/web/Microsoft.Samples.Cosmos.Table.Quickstart.Web.csproj** file to validate that the `Azure.Data.Tables` entry exists.

### Import libraries

Import the `Azure.Identity` and `Azure.Data.Tables` namespaces into your application code.

```csharp
using Azure.Identity;

using Azure.Data.Tables;
```

## Object model

| Name | Description |
| --- | --- |
| <xref:Azure.Data.Tables.TableServiceClient> | This class is the primary client class and is used to manage account-wide metadata or databases. |
| <xref:Azure.Data.Tables.TableClient> | This class represents the client for a table within the account. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a table](#get-a-table)
- [Create an entity](#create-an-entity)
- [Get an entity](#get-an-entity)
- [Query entities](#query-entities)

The sample code in the template uses a table named `cosmicworks-products`. The `cosmicworks-products` table contains details such as name, category, quantity, price, a unique identifier, and a sale flag for each product. The container uses a *unique identifier* as the row key and *category* as a partition key.

### Authenticate the client

This sample creates a new instance of the `TableServiceClient` class.

```csharp
DefaultAzureCredential credential = new();

TableServiceClient serviceClient = new(
    endpoint: new Uri("<azure-cosmos-db-table-account-endpoint>"),
    credential
);
```

### Get a table

This sample creates an instance of the `TableClient` class using the `GetTableClient` method of the `TableServiceClient` class.

```csharp
TableClient client = serviceClient.GetTableClient(
    tableName: "<azure-cosmos-db-table-name>"
);
```

### Create an entity

The easiest way to create a new entity in a table is to create a class that implements the `ITableEntity` interface. You can then add your own properties to the class to populate columns of data in that table row.

```csharp
public record Product : ITableEntity
{
    public required string RowKey { get; set; }

    public required string PartitionKey { get; set; }

    public required string Name { get; set; }

    public required int Quantity { get; set; }

    public required decimal Price { get; set; }

    public required bool Clearance { get; set; }

    public ETag ETag { get; set; } = ETag.All;

    public DateTimeOffset? Timestamp { get; set; }
};
```

Create an entity in the table using the `Product` class by calling `TableClient.AddEntityAsync<T>`.

```csharp
Product entity = new()
{
    RowKey = "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
    PartitionKey = "gear-surf-surfboards",
    Name = "Surfboard",
    Quantity = 10,
    Price = 300.00m,
    Clearance = true
};

Response response = await client.UpsertEntityAsync<Product>(
    entity: entity,
    mode: TableUpdateMode.Replace
);
```

### Get an entity

You can retrieve a specific entity from a table using the `TableClient.GetEntityAsync<T>` method. Provide the `partitionKey` and `rowKey` as parameters to identify the correct row to perform a quick *point read* of that entity.

```csharp
Response<Product> response = await client.GetEntityAsync<Product>(
    rowKey: "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
    partitionKey: "gear-surf-surfboards"
);
```

### Query entities

After you insert an entity, you can also run a query to get all entities that match a specific filter by using the `TableClient.Query<T>` method. This example filters products by category using Language Integrated Query (LINQ) syntax, which is a benefit of using typed `ITableEntity` models like the `Product` class.

```csharp
string category = "gear-surf-surfboards";

AsyncPageable<Product> results = client.QueryAsync<Product>(
    product => product.PartitionKey == category
);
```

Parse the paginated results of the query by looping through each page of results using asynchronous loop.

```csharp
List<Product> entities = new();
await foreach (Product product in results)
{
    entities.Add(product);
}
```

## Clean up resources

When you no longer need the sample application or resources, remove the corresponding deployment and all resources.

```azurecli
azd down
```

## Related content

- [Node.js Quickstart](quickstart-nodejs.md)
- [Python Quickstart](quickstart-python.md)
- [Java Quickstart](quickstart-java.md)
- [Go Quickstart](quickstart-go.md)
