---
title: Quickstart - Azure Cosmos DB for Table for .NET
description: Learn how to build a .NET app to manage Azure Cosmos DB for Table resources in this quickstart.
author: seesharprun
ms.author: sasinnat
ms.service: azure-cosmos-db
ms.subservice: table
ms.devlang: csharp
ms.topic: quickstart
ms.date: 10/07/2024
ms.custom: devx-track-csharp, ignite-2022, devguide-csharp, cosmos-db-dev-journey, devx-track-dotnet, devx-track-extended-azdevcli
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

:::code language="csharp" source="~/cosmos-db-table-dotnet-quickstart/src/web/Program.cs" id="create_client":::

### Create an item

The easiest way to create a new item in a table is to create a class that implements the [``ITableEntity``](/dotnet/api/azure.data.tables.itableentity) interface. You can then add your own properties to the class to populate columns of data in that table row.

:::code language="csharp" source="~/cosmos-db-table-dotnet-quickstart/src/web/Models/Product.cs" id="model":::

Create an item in the collection using the `Product` class by calling [``TableClient.AddEntityAsync<T>``](/dotnet/api/azure.data.tables.tableclient.addentityasync).

:::code language="csharp" source="~/cosmos-db-table-dotnet-quickstart/src/web/Services/DemoService.cs" id="create_entity":::

### Get an item

You can retrieve a specific item from a table using the [``TableClient.GetEntityAsync<T>``](/dotnet/api/azure.data.tables.tableclient.getentity) method. Provide the `partitionKey` and `rowKey` as parameters to identify the correct row to perform a quick *point read* of that item.

:::code language="csharp" source="~/cosmos-db-table-dotnet-quickstart/src/web/Services/DemoService.cs" id="read_entity":::

### Query items

After you insert an item, you can also run a query to get all items that match a specific filter by using the `TableClient.Query<T>` method. This example filters products by category using [Linq](/dotnet/standard/linq) syntax, which is a benefit of using typed `ITableEntity` models like the `Product` class.

> [!NOTE]
> You can also query items using [OData](/rest/api/storageservices/querying-tables-and-entities) syntax. You can see an example of this approach in the [Query Data](./tutorial-query.md) tutorial.

:::code language="csharp" source="~/cosmos-db-table-dotnet-quickstart/src/web/Services/DemoService.cs" id="query_entities":::

Parse the paginated results of the query by looping through each page of results using asynchronous loop to determine if there are any results left at the start of each loop.

:::code language="csharp" source="~/cosmos-db-table-dotnet-quickstart/src/web/Services/DemoService.cs" id="parse_results":::

## Run the code

This app creates an Azure Cosmos DB Table API table. The example then creates an item and then reads the exact same item back. Finally, the example creates a second item and then performs a query that should return multiple items. With each step, the example outputs metadata to the console about the steps it performed.

To run the app, use a terminal to navigate to the application directory and run the application.

```dotnetcli
dotnet run
```

The output of the app should be similar to this example:

```output
Single product name: 
Yamba Surfboard
Multiple products:
Yamba Surfboard
Sand Surfboard
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

## Next steps

In this quickstart, you learned how to create an Azure Cosmos DB for Table account, create a table, and manage entries using the .NET SDK. You can now dive deeper into the SDK to learn how to perform more advanced data queries and management tasks in your Azure Cosmos DB for Table resources.

> [!div class="nextstepaction"]
> [Get started with Azure Cosmos DB for Table and .NET](./how-to-dotnet-get-started.md)
