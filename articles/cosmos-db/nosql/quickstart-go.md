---
title: Quickstart - Azure SDK for Go
titleSuffix: Azure Cosmos DB for NoSQL
description: Deploy a Go web application that uses the Azure SDK for Go to interact with Azure Cosmos DB for NoSQL data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.devlang: golang
ms.topic: quickstart-sdk
ms.date: 06/11/2025
ms.custom: devx-track-go, devx-track-extended-azdevcli
appliesto:
  - ✅ NoSQL
# CustomerIntent: As a developer, I want to learn the basics of the Go library so that I can build applications with Azure Cosmos DB for NoSQL.
---

# Quickstart: Use Azure Cosmos DB for NoSQL with Azure SDK for Go

[!INCLUDE[Developer Quickstart selector](includes/quickstart/dev-selector.md)]

In this quickstart, you deploy a basic Azure Cosmos DB for NoSQL application using the Azure SDK for Go. Azure Cosmos DB for NoSQL is a schemaless data store allowing applications to store unstructured data in the cloud. Query data in your containers and perform common operations on individual items using the Azure SDK for Go.

[API reference documentation](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos) | [Library source code](https://github.com/Azure/azure-sdk-for-go/tree/main/sdk/data/azcosmos#readme) | [Package (Go)](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

- Azure Developer CLI
- Docker Desktop
- `Go` 1.21 or newer

If you don't have an Azure account, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Initialize the project

Use the Azure Developer CLI (`azd`) to create an Azure Cosmos DB for NoSQL account and deploy a containerized sample application. The sample application uses the client library to manage, create, read, and query sample data.

1. Open a terminal in an empty directory.

1. If you're not already authenticated, authenticate to the Azure Developer CLI using `azd auth login`. Follow the steps specified by the tool to authenticate to the CLI using your preferred Azure credentials.

    ```azurecli
    azd auth login
    ```

1. Use `azd init` to initialize the project.

    ```azurecli
    azd init --template cosmos-db-nosql-go-quickstart
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

:::image type="content" source="media/quickstart-go/running-application.png" alt-text="Screenshot of the running web application.":::

### Install the client library

The client library is available through Go, as the `azcosmos` package.

1. Open a terminal and navigate to the `/src` folder.

    ```bash
    cd ./src
    ```

1. If not already installed, install the `azcosmos` package using `go install`.

    ```bash
    go install github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos
    ```

1. Also, install the `azidentity` package if not already installed.

    ```bash
    go install github.com/Azure/azure-sdk-for-go/sdk/azidentity
    ```

1. Open and review the **src/go.mod** file to validate that the `github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos` and `github.com/Azure/azure-sdk-for-go/sdk/azidentity` entries both exist.

### Import libraries

Import the `github.com/Azure/azure-sdk-for-go/sdk/azidentity` and `github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos` packages into your application code.

```go
import (
	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
	"github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos"
)
```

## Object model

| Name | Description |
| --- | --- |
| [`CosmosClient`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos#CosmosClient) | This class is the primary client class and is used to manage account-wide metadata or databases. |
| [`CosmosDatabase`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos#CosmosDatabase) | This class represents a database within the account. |
| [`CosmosContainer`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos#CosmosContainer) | This class is primarily used to perform read, update, and delete operations on either the container or the items stored within the container. |
| [`PartitionKey`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos#PartitionKey) | This class represents a logical partition key. This class is required for many common operations and queries. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a database](#get-a-database)
- [Get a container](#get-a-container)
- [Create an item](#create-an-item)
- [Get an item](#read-an-item)
- [Query items](#query-items)

The sample code in the template uses a database named `cosmicworks` and container named `products`. The `products` container contains details such as name, category, quantity, a unique identifier, and a sale flag for each product. The container uses the `/category` property as a logical partition key.

### Authenticate the client

This sample creates a new instance of `CosmosClient` using `azcosmos.NewClient` and authenticates using a `DefaultAzureCredential` instance.

```go
credential, err := azidentity.NewDefaultAzureCredential(nil)
if err != nil {
    return err
}

clientOptions := azcosmos.ClientOptions{
    EnableContentResponseOnWrite: true,
}

client, err := azcosmos.NewClient("<azure-cosmos-db-nosql-account-endpoint>", credential, &clientOptions)
if err != nil {
    return err
}
```

### Get a database

Use `client.NewDatabase` to retrieve the existing database named *`cosmicworks`*.

```go
database, err := client.NewDatabase("cosmicworks")
if err != nil {
    return err
}
```

### Get a container

Retrieve the existing *`products`* container using `database.NewContainer`.

```go
container, err := database.NewContainer("products")
if err != nil {
    return err
}
```

### Create an item

Build a Go type with all of the members you want to serialize into JSON. In this example, the type has a unique identifier, and fields for category, name, quantity, price, and sale.

```go
type Item struct {
  Id        string  `json:"id"`
  Category  string  `json:"category"`
  Name      string  `json:"name"`
  Quantity  int     `json:"quantity"`
  Price     float32 `json:"price"`
  Clearance bool    `json:"clearance"`
}
```

Create an item in the container using `container.UpsertItem`. This method "upserts" the item effectively replacing the item if it already exists.

```go
item := Item {
    Id:        "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
    Category:  "gear-surf-surfboards",
    Name:      "Yamba Surfboard",
    Quantity:  12,
    Price:     850.00,
    Clearance: false,
}

partitionKey := azcosmos.NewPartitionKeyString("gear-surf-surfboards")

context := context.TODO()

bytes, err := json.Marshal(item)
if err != nil {
    return err
}

response, err := container.UpsertItem(context, partitionKey, bytes, nil)
if err != nil {
    return err
}
```

### Read an item

Perform a point read operation by using both the unique identifier (`id`) and partition key fields. Use `container.ReadItem` to efficiently retrieve the specific item.

```go
partitionKey := azcosmos.NewPartitionKeyString("gear-surf-surfboards")

context := context.TODO()

itemId := "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"

response, err := container.ReadItem(context, partitionKey, itemId, nil)
if err != nil {
    return err
}

if response.RawResponse.StatusCode == 200 {
    read_item := Item{}
    err := json.Unmarshal(response.Value, &read_item)
    if err != nil {
        return err
    }
}
```

### Query items

Perform a query over multiple items in a container using `container.NewQueryItemsPager`. Find all items within a specified category using this parameterized query:

```nosql
SELECT * FROM products p WHERE p.category = @category
```

```go
partitionKey := azcosmos.NewPartitionKeyString("gear-surf-surfboards")

query := "SELECT * FROM products p WHERE p.category = @category"

queryOptions := azcosmos.QueryOptions{
    QueryParameters: []azcosmos.QueryParameter{
        {Name: "@category", Value: "gear-surf-surfboards"},
    },
}

pager := container.NewQueryItemsPager(query, partitionKey, &queryOptions)
```

Parse the paginated results of the query by looping through each page of results using `pager.NextPage`. Use `pager.More` to determine if there are any results left at the start of each loop.

```go
items := []Item{}

for pager.More() {
    response, err := pager.NextPage(context.TODO())
    if err != nil {
        return err
    }

    for _, bytes := range response.Items {
        item := Item{}
        err := json.Unmarshal(bytes, &item)
        if err != nil {
            return err
        }
        items = append(items, item)
    }
}
```

### Explore your data

Use the Visual Studio Code extension for Azure Cosmos DB to explore your NoSQL data. You can perform core database operations including, but not limited to:

- Performing queries using a scrapbook or the query editor
- Modifying, updating, creating, and deleting items
- Importing bulk data from other sources
- Managing databases and containers

For more information, see [How-to use Visual Studio Code extension to explore Azure Cosmos DB for NoSQL data](../visual-studio-code-extension.md?pivots=api-nosql).

## Clean up resources

When you no longer need the sample application or resources, remove the corresponding deployment and all resources.

```azurecli
azd down
```

## Related content

- [.NET Quickstart](quickstart-dotnet.md)
- [Node.js Quickstart](quickstart-nodejs.md)
- [Java Quickstart](quickstart-java.md)
- [Python Quickstart](quickstart-python.md)
- [Rust Quickstart](quickstart-go.md)
