---
title: Quickstart - .NET client library
titleSuffix: Azure Cosmos DB for Table
description: Deploy a .NET web application that uses the client library to interact with Azure Cosmos DB for Table data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: table
ms.devlang: csharp
ms.topic: quickstart
ms.date: 10/15/2024
ms.custom: devx-track-csharp, devx-track-dotnet, devx-track-extended-azdevcli
zone_pivot_groups: azure-cosmos-db-quickstart-env
---

# Quickstart: Azure Cosmos DB for Table for .NET

[!INCLUDE[Table](../includes/appliesto-table.md)]

> [!div class="op_single_selector"]
>
> * [.NET](quickstart-dotnet.md)
> * [Java](quickstart-java.md)
> * [Node.js](quickstart-nodejs.md)
> * [Python](quickstart-python.md)
>

This quickstart shows how to get started with the Azure Cosmos DB for Table from a .NET application. The Azure Cosmos DB for Table is a schemaless data store allowing applications to store structured table data in the cloud. You learn how to create tables, rows, and perform basic tasks within your Azure Cosmos DB resource using the [Azure.Data.Tables Package (NuGet)](https://www.nuget.org/packages/Azure.Data.Tables/).

> [!NOTE]
> The [example code snippets](https://github.com/Azure-Samples/cosmos-db-table-api-dotnet-samples) are available on GitHub as a .NET project.

[API for Table reference documentation](/azure/storage/tables/) | [Azure.Data.Tables Package (NuGet)](https://www.nuget.org/packages/Azure.Data.Tables/)

## Prerequisites

[!INCLUDE[Developer Quickstart prerequisites](includes/quickstart/dev-prereqs.md)]

## Setting up

Deploy this project's development container to your environment. Then, use the Azure Developer CLI (azd) to create an Azure Cosmos DB for Table account and deploy a containerized sample application. The sample application uses the client library to manage, create, read, and query sample data.

::: zone pivot="devcontainer-codespace"

[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=brightgreen&logo=github)](https://codespaces.new/Azure-Samples/cosmos-db-table-dotnet-quickstart?template=false&quickstart=1&azure-portal=true)

::: zone-end

::: zone pivot="devcontainer-vscode"

[![Open in Dev Container](https://img.shields.io/static/v1?style=for-the-badge&label=Dev+Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/cosmos-db-table-dotnet-quickstart)

::: zone-end

[!INCLUDE[Developer Quickstart setup](includes/quickstart/dev-setup.md)]

### Install the client library

The client library is available through NuGet, as the `Microsoft.Azure.Cosmos` package.

1. Open a terminal and navigate to the `/src/web` folder.

    ```bash
    cd ./src/web
    ```

1. If not already installed, install the `Azure.Data.Tables` package using `dotnet add package`.

    ```bash
    dotnet add package Azure.Data.Tables --version 12.*
    ```

1. Also, install the `Azure.Identity` package if not already installed.

    ```bash
    dotnet add package Azure.Identity --version 1.*
    ```

1. Open and review the **src/web/Cosmos.Samples.Table.Quickstart.Web.csproj** file to validate that the `Azure.Data.Tables` and `Azure.Identity` entries both exist.

## Object model

| Name | Description |
| --- | --- |
| <xref:Azure.Data.Tables.TableServiceClient> | This class is the primary client class and is used to manage account-wide metadata or databases. |
| <xref:Azure.Data.Tables.TableClient> | This class represents the client for a table within the account. |

## Code examples

* [Authenticate the clients](#authenticate-the-clients)
* [Create an item](#create-an-item)
* [Get an item](#get-an-item)
* [Query items](#query-items)

The sample code in the template uses a table named `cosmicworks-products`. The table contains details such as name, category, quantity, a unique identifier, and a sale flag for each product.

### Authenticate the clients

Application requests to most Azure services must be authorized. Use the `DefaultAzureCredential` type as the preferred way to implement a passwordless connection between your applications and Azure Cosmos DB for NoSQL. `DefaultAzureCredential` supports multiple authentication methods and determines which method should be used at runtime.

> [!IMPORTANT]
> You can also authorize requests to Azure services using passwords, connection strings, or other credentials directly. However, this approach should be used with caution. Developers must be diligent to never expose these secrets in an unsecure location. Anyone who gains access to the password or secret key is able to authenticate to the database service. `DefaultAzureCredential` offers improved management and security benefits over the account key to allow passwordless authentication without the risk of storing keys.

This sample creates a new instance of the `TableServiceClient` and `TableClient` classes and authenticates using a `DefaultAzureCredential` instance.

```csharp
DefaultAzureCredential credential = new();

TableServiceClient serviceClient = new(
    endpoint: new Uri("<azure-cosmos-db-table-account-endpoint>"),
    tokenCredential: credential
);

TableClient client = serviceClient.GetTableClient(
    tableName: "<azure-cosmos-db-table-name>"
);
```

### Create an item

The easiest way to create a new item in a table is to create a class that implements the [``ITableEntity``](/dotnet/api/azure.data.tables.itableentity) interface. You can then add your own properties to the class to populate columns of data in that table row.

```csharp
public record Product : ITableEntity
{
    public string RowKey { get; set; } = $"{Guid.NewGuid()}";

    public string PartitionKey { get; set; } = String.Empty;

    public string Name { get; set; } = String.Empty;

    public int Quantity { get; set; } = 0;

    public decimal Price { get; set; } = 0.0m;

    public bool Clearance { get; set; } = false;

    public ETag ETag { get; set; } = ETag.All;

    public DateTimeOffset? Timestamp { get; set; }
};
```

Create an item in the collection using the `Product` class by calling [``TableClient.AddEntityAsync<T>``](/dotnet/api/azure.data.tables.tableclient.addentityasync).

```csharp
Product entity = new()
{
    RowKey = "68719518391",
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

### Get an item

You can retrieve a specific item from a table using the [``TableClient.GetEntityAsync<T>``](/dotnet/api/azure.data.tables.tableclient.getentity) method. Provide the `partitionKey` and `rowKey` as parameters to identify the correct row to perform a quick *point read* of that item.

```csharp
Response<Product> response = await client.GetEntityAsync<Product>(
    rowKey: "68719518391",
    partitionKey: "gear-surf-surfboards"
);
```

### Query items

After you insert an item, you can also run a query to get all items that match a specific filter by using the `TableClient.Query<T>` method. This example filters products by category using [Linq](/dotnet/standard/linq) syntax, which is a benefit of using typed `ITableEntity` models like the `Product` class.

> [!NOTE]
> You can also query items using [OData](/rest/api/storageservices/querying-tables-and-entities) syntax. You can see an example of this approach in the [Query Data](./tutorial-query.md) tutorial.

```csharp
string category = "gear-surf-surfboards";

AsyncPageable<Product> results = client.QueryAsync<Product>(
    product => product.PartitionKey == category
);
```

Parse the paginated results of the query by looping through each page of results using asynchronous loop to determine if there are any results left at the start of each loop.

```csharp

```

## Clean up resources

When you no longer need the Azure Cosmos DB for Table account, you can delete the corresponding resource group.

### [Azure CLI](#tab/azure-cli)

Use the [``az group delete``](/cli/azure/group#az-group-delete) command to delete the resource group.

```azurecli-interactive
az group delete --name $resourceGroupName
```

### [PowerShell](#tab/azure-powershell)

Use the [``Remove-AzResourceGroup``](/powershell/module/az.resources/remove-azresourcegroup) cmdlet to delete the resource group.

```azurepowershell-interactive
$parameters = @{
    Name = $RESOURCE_GROUP_NAME
}
Remove-AzResourceGroup @parameters
```

### [Portal](#tab/azure-portal)

1. Navigate to the resource group you previously created in the Azure portal.

    > [!TIP]
    > In this quickstart, we recommended the name ``msdocs-cosmos-quickstart-rg``.
1. Select **Delete resource group**.

   :::image type="content" source="media/dotnet-quickstart/delete-resource-group-option.png"  alt-text="Screenshot of the resource group deletion option in the navigation bar for a resource group.":::

1. On the **Are you sure you want to delete** dialog, enter the name of the resource group, and then select **Delete**.

   :::image type="content" source="media/dotnet-quickstart/delete-confirmation.png" alt-text="Screenshot of the confirmation page for the deletion of a resource group.":::

---

## Related content

- [Node.js Quickstart](quickstart-nodejs.md)
- [Python Quickstart](quickstart-python.md)
- [Java Quickstart](quickstart-java.md)

## Next step

> [!div class="nextstepaction"]
> [Get started with Azure Cosmos DB for Table and .NET](./how-to-dotnet-get-started.md)
